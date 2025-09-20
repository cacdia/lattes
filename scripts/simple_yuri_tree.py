#!/usr/bin/env python3
"""
Script para gerar uma visualização simples e didática do grafo do professor Yuri.
Estrutura de árvore limpa e fácil de entender.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import numpy as np
from typing import Dict, List


def load_publications_data() -> List[Dict]:
    """Carrega os dados de publicações unificadas."""
    with open("data/publicacoes_unificadas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_simple_tree(publications: List[Dict]) -> nx.Graph:
    """
    Cria uma árvore simples centrada no Yuri com apenas colaboradores importantes.
    """
    G = nx.Graph()
    yuri_name = "Yuri de Almeida Malheiros Barbosa"

    # Encontra todas as publicações do Yuri
    yuri_publications = []
    for pub in publications:
        if yuri_name in pub.get("professores", []):
            yuri_publications.append(pub)

    # Conta colaborações do Yuri
    yuri_collaborations = defaultdict(int)
    for pub in yuri_publications:
        for prof in pub["professores"]:
            if prof != yuri_name:
                yuri_collaborations[prof] += 1

    # Filtra apenas colaboradores com 5+ colaborações para simplificar
    important_collaborators = {
        prof: count for prof, count in yuri_collaborations.items() if count >= 5
    }

    # Adiciona Yuri como nó central
    G.add_node(yuri_name, collaborations=sum(yuri_collaborations.values()))

    # Adiciona apenas colaboradores importantes
    for prof, count in important_collaborators.items():
        G.add_node(prof, collaborations=count)
        G.add_edge(yuri_name, prof, weight=count)

    return G, important_collaborators


def create_tree_visualization(
    G: nx.Graph, collaborators: Dict[str, int], output_file: str
):
    """
    Cria uma visualização simples de árvore.
    """
    # Configuração da figura
    plt.figure(figsize=(16, 12))
    plt.style.use("default")

    # Layout hierárquico (árvore)
    pos = nx.spring_layout(G, k=4, iterations=100, seed=42)

    # Ajusta posição do Yuri para o centro
    yuri_name = "Yuri de Almeida Malheiros Barbosa"
    if yuri_name in pos:
        # Move Yuri para o centro
        pos[yuri_name] = (0, 0)

        # Organiza colaboradores em círculo ao redor do Yuri
        collaborators_list = [n for n in G.nodes() if n != yuri_name]
        n_collaborators = len(collaborators_list)

        if n_collaborators > 0:
            # Cria posições em círculo
            angles = np.linspace(0, 2 * np.pi, n_collaborators, endpoint=False)
            radius = 2.5

            for i, collab in enumerate(collaborators_list):
                x = radius * np.cos(angles[i])
                y = radius * np.sin(angles[i])
                pos[collab] = (x, y)

    # Tamanhos dos nós
    node_sizes = []
    for node in G.nodes():
        if node == yuri_name:
            node_sizes.append(2000)  # Yuri maior
        else:
            collabs = collaborators.get(node, 1)
            # Tamanho baseado em colaborações (escala mais suave)
            node_sizes.append(max(400, 800 * np.log(collabs + 1)))

    # Cores simples
    node_colors = []
    for node in G.nodes():
        if node == yuri_name:
            node_colors.append("#FFD700")  # Dourado para Yuri
        else:
            collabs = collaborators.get(node, 1)
            if collabs >= 20:
                node_colors.append("#FF6B6B")  # Vermelho para alta colaboração
            else:
                node_colors.append("#4ECDC4")  # Verde-azulado para média colaboração

    # Desenha os nós
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=G.nodes(),
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
        edgecolors="black",
        linewidths=2,
    )

    # Desenha as arestas
    edges = G.edges()
    weights = [G[u][v]["weight"] for u, v in edges]
    max_weight = max(weights) if weights else 1

    # Espessura das arestas baseada no peso
    edge_widths = [max(2, 6 * w / max_weight) for w in weights]

    nx.draw_networkx_edges(
        G, pos, edgelist=edges, width=edge_widths, alpha=0.7, edge_color="gray"
    )

    # Labels simplificados
    labels = {}
    for node in G.nodes():
        if node == yuri_name:
            labels[node] = "YURI\n(232 colabs)"
        else:
            collabs = collaborators.get(node, 0)
            # Nome simplificado (apenas sobrenome)
            name_parts = node.split()
            if len(name_parts) >= 2:
                short_name = f"{name_parts[-2]} {name_parts[-1]}"
            else:
                short_name = node
            labels[node] = f"{short_name}\n({collabs})"

    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")

    # Título simples
    plt.title(
        "ÁRVORE DE COLABORAÇÕES - PROFESSOR YURI",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )

    # Legenda simplificada
    legend_elements = [
        mpatches.Patch(color="#FFD700", label="Yuri (Centro)"),
        mpatches.Patch(color="#FF6B6B", label="Alta Colaboração (≥20)"),
        mpatches.Patch(color="#4ECDC4", label="Média Colaboração (5-19)"),
    ]

    plt.legend(handles=legend_elements, loc="upper right", fontsize=12)

    # Remove eixos
    plt.axis("off")

    # Ajusta layout
    plt.tight_layout()

    # Salva a imagem
    plt.savefig(
        output_file, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none"
    )

    print(f"✅ Árvore simplificada salva em: {output_file}")

    # Mostra estatísticas
    print(f"\n📊 Estatísticas da Árvore:")
    print(f"   • Total de nós: {G.number_of_nodes()}")
    print(f"   • Colaboradores importantes: {len(collaborators)}")
    print(f"   • Colaborações totais: {sum(collaborators.values())}")

    # Top colaboradores
    top_collaborators = sorted(collaborators.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]
    print(f"\n🏆 Top Colaboradores:")
    for i, (name, count) in enumerate(top_collaborators, 1):
        print(f"   {i}. {name}: {count} colaborações")


def main():
    """Função principal."""
    print("🌳 Gerando árvore simplificada do professor Yuri...")

    # Carrega os dados
    publications = load_publications_data()

    print("📊 Criando árvore de colaborações...")
    G, collaborators = create_simple_tree(publications)

    print("🎨 Criando visualização...")
    output_file = "data/yuri_simple_tree.png"
    create_tree_visualization(G, collaborators, output_file)

    print(f"\n🎯 Árvore simplificada concluída! Verifique: {output_file}")


if __name__ == "__main__":
    main()
