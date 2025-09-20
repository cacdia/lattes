#!/usr/bin/env python3
"""
Script para gerar visualização gráfica do grafo de colaborações do professor Yuri.
Usa NetworkX e Matplotlib para criar uma imagem visual.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import numpy as np
from typing import Dict, List, Tuple


def load_publications_data() -> List[Dict]:
    """Carrega os dados de publicações unificadas."""
    with open("data/publicacoes_unificadas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_collaboration_graph(publications: List[Dict]) -> nx.Graph:
    """
    Cria um grafo de colaborações baseado nas publicações.
    """
    G = nx.Graph()
    collaboration_weights = defaultdict(int)

    # Adiciona todas as colaborações
    for pub in publications:
        professores = pub.get("professores", [])

        # Cria arestas entre todos os pares de professores na publicação
        for i, prof1 in enumerate(professores):
            for prof2 in professores[i + 1 :]:
                # Adiciona peso à colaboração
                edge = tuple(sorted([prof1, prof2]))
                collaboration_weights[edge] += 1

    # Adiciona nós e arestas ao grafo
    for (prof1, prof2), weight in collaboration_weights.items():
        G.add_edge(prof1, prof2, weight=weight)

    return G, collaboration_weights


def create_yuri_centered_graph(publications: List[Dict]) -> nx.Graph:
    """
    Cria um grafo centrado no Yuri com seus colaboradores diretos.
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

    # Adiciona Yuri como nó central
    G.add_node(
        yuri_name, node_type="root", collaborations=sum(yuri_collaborations.values())
    )

    # Adiciona colaboradores e suas conexões com Yuri
    for prof, count in yuri_collaborations.items():
        G.add_node(prof, node_type="collaborator", collaborations=count)
        G.add_edge(yuri_name, prof, weight=count)

    return G, yuri_collaborations


def create_visualization(
    G: nx.Graph, yuri_collaborations: Dict[str, int], output_file: str
):
    """
    Cria a visualização gráfica do grafo.
    """
    # Configuração da figura
    plt.figure(figsize=(20, 16))
    plt.style.use("default")

    # Layout do grafo
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

    # Separa nós por tipo
    root_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "root"]
    collaborator_nodes = [
        n for n, d in G.nodes(data=True) if d.get("node_type") == "collaborator"
    ]

    # Tamanhos dos nós baseados no número de colaborações
    node_sizes = []
    for node in G.nodes():
        if node == "Yuri de Almeida Malheiros Barbosa":
            node_sizes.append(3000)  # Nó central maior
        else:
            collabs = yuri_collaborations.get(node, 1)
            # Escala logarítmica para melhor visualização
            node_sizes.append(max(200, 500 * np.log(collabs + 1)))

    # Cores dos nós baseadas no número de colaborações
    node_colors = []
    for node in G.nodes():
        if node == "Yuri de Almeida Malheiros Barbosa":
            node_colors.append("#FFD700")  # Dourado para Yuri
        else:
            collabs = yuri_collaborations.get(node, 1)
            if collabs >= 20:
                node_colors.append("#FF6B6B")  # Vermelho para alta colaboração
            elif collabs >= 10:
                node_colors.append("#4ECDC4")  # Verde-azulado para média colaboração
            elif collabs >= 5:
                node_colors.append("#45B7D1")  # Azul para baixa colaboração
            else:
                node_colors.append("#96CEB4")  # Verde claro para muito baixa

    # Desenha o grafo
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=G.nodes(),
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.8,
        edgecolors="black",
        linewidths=2,
    )

    # Desenha as arestas com espessura baseada no peso
    edges = G.edges()
    weights = [G[u][v]["weight"] for u, v in edges]
    max_weight = max(weights) if weights else 1

    # Escala as espessuras das arestas
    edge_widths = [max(1, 8 * w / max_weight) for w in weights]

    nx.draw_networkx_edges(
        G, pos, edgelist=edges, width=edge_widths, alpha=0.6, edge_color="gray"
    )

    # Adiciona labels apenas para nós importantes
    important_nodes = [
        n
        for n, d in G.nodes(data=True)
        if d.get("collaborations", 0) >= 10 or n == "Yuri de Almeida Malheiros Barbosa"
    ]

    labels = {}
    for node in important_nodes:
        if node == "Yuri de Almeida Malheiros Barbosa":
            labels[node] = "YURI\n(232 colabs)"
        else:
            collabs = yuri_collaborations.get(node, 0)
            # Trunca nome se muito longo
            short_name = (
                node.split()[-2] + " " + node.split()[-1]
                if len(node.split()) > 2
                else node
            )
            labels[node] = f"{short_name}\n({collabs} colabs)"

    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")

    # Título e configurações
    plt.title(
        "🌳 GRAFO DE COLABORAÇÕES - PROFESSOR YURI DE ALMEIDA MALHEIROS BARBOSA",
        fontsize=20,
        fontweight="bold",
        pad=20,
    )

    # Legenda
    legend_elements = [
        mpatches.Patch(color="#FFD700", label="Yuri (Raiz)"),
        mpatches.Patch(color="#FF6B6B", label="Alta Colaboração (≥20)"),
        mpatches.Patch(color="#4ECDC4", label="Média Colaboração (10-19)"),
        mpatches.Patch(color="#45B7D1", label="Baixa Colaboração (5-9)"),
        mpatches.Patch(color="#96CEB4", label="Muito Baixa (<5)"),
    ]

    plt.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1, 1))

    # Remove eixos
    plt.axis("off")

    # Ajusta layout
    plt.tight_layout()

    # Salva a imagem
    plt.savefig(
        output_file, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none"
    )

    print(f"✅ Visualização salva em: {output_file}")

    # Mostra estatísticas
    print(f"\n📊 Estatísticas do Grafo:")
    print(f"   • Total de nós: {G.number_of_nodes()}")
    print(f"   • Total de arestas: {G.number_of_edges()}")
    print(f"   • Colaboradores únicos: {len(yuri_collaborations)}")
    print(f"   • Colaborações totais: {sum(yuri_collaborations.values())}")

    # Top 5 colaboradores
    top_collaborators = sorted(
        yuri_collaborations.items(), key=lambda x: x[1], reverse=True
    )[:5]
    print(f"\n🏆 Top 5 Colaboradores:")
    for i, (name, count) in enumerate(top_collaborators, 1):
        print(f"   {i}. {name}: {count} colaborações")


def create_network_analysis(G: nx.Graph, yuri_collaborations: Dict[str, int]) -> Dict:
    """
    Realiza análise de rede do grafo.
    """
    analysis = {}

    # Centralidade de grau
    degree_centrality = nx.degree_centrality(G)
    analysis["degree_centrality"] = degree_centrality

    # Centralidade de intermediação
    betweenness_centrality = nx.betweenness_centrality(G)
    analysis["betweenness_centrality"] = betweenness_centrality

    # Densidade do grafo
    analysis["density"] = nx.density(G)

    # Coeficiente de clustering
    analysis["clustering"] = nx.average_clustering(G)

    return analysis


def main():
    """Função principal."""
    print("🎨 Gerando visualização gráfica do grafo do professor Yuri...")

    # Carrega os dados
    publications = load_publications_data()

    print("📊 Criando grafo de colaborações...")
    G, yuri_collaborations = create_yuri_centered_graph(publications)

    print("🔍 Realizando análise de rede...")
    analysis = create_network_analysis(G, yuri_collaborations)

    print("🎨 Criando visualização...")
    output_file = "data/yuri_collaboration_graph.png"
    create_visualization(G, yuri_collaborations, output_file)

    # Salva análise em JSON
    analysis_file = "data/yuri_network_analysis.json"
    with open(analysis_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"📊 Análise de rede salva em: {analysis_file}")
    print(f"\n🎯 Visualização concluída! Verifique o arquivo: {output_file}")


if __name__ == "__main__":
    main()
