#!/usr/bin/env python3
"""
Script para gerar uma representação visual do heap do professor Yuri.
Cria um desenho ASCII e também salva um arquivo de texto com a estrutura.
"""

import json
from typing import List, Dict


def load_heap_data() -> Dict:
    """Carrega os dados do heap do Yuri."""
    with open("data/professor_yuri_heap.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_ascii_heap(heap_data: Dict) -> str:
    """
    Cria uma representação ASCII do heap.
    """
    heap = heap_data["heap"]
    if not heap:
        return "Heap vazio!"

    # Encontra a altura máxima do heap
    max_height = heap_data["properties"]["heap_height"]

    # Cria a representação
    lines = []
    lines.append("=" * 80)
    lines.append(
        "🌳 HEAP DE COLABORAÇÕES - PROFESSOR YURI DE ALMEIDA MALHEIROS BARBOSA"
    )
    lines.append("=" * 80)
    lines.append("")

    # Desenha o heap nível por nível
    current_index = 0
    level = 0

    while current_index < len(heap):
        # Calcula quantos nós existem neste nível
        nodes_in_level = min(2**level, len(heap) - current_index)

        # Espaçamento baseado no nível
        indent = " " * (2 ** (max_height - level - 1) * 4)
        spacing = " " * (2 ** (max_height - level) * 4)

        # Desenha os nós do nível atual
        level_nodes = []
        for i in range(nodes_in_level):
            if current_index + i < len(heap):
                node = heap[current_index + i]
                name = node["name"]
                collabs = node["collaborations"]

                # Trunca nome se muito longo
                if len(name) > 25:
                    name = name[:22] + "..."

                # Formata o nó
                if node["is_root"]:
                    node_str = f"👑 {name} ({collabs})"
                else:
                    node_str = f"👤 {name} ({collabs})"

                level_nodes.append(node_str)

        # Adiciona a linha do nível
        lines.append(indent + spacing.join(level_nodes))

        # Adiciona linhas de conexão se não for o último nível
        if level < max_height - 1 and current_index + nodes_in_level < len(heap):
            connection_line = indent
            for i in range(nodes_in_level):
                if i > 0:
                    connection_line += spacing
                if i % 2 == 0:  # Nó esquerdo
                    connection_line += "  ╚═══╗"
                else:  # Nó direito
                    connection_line += "  ╔═══╝"
            lines.append(connection_line)

        current_index += nodes_in_level
        level += 1

    lines.append("")
    lines.append("=" * 80)
    lines.append("📊 LEGENDA:")
    lines.append("👑 = Raiz (Professor Yuri)")
    lines.append("👤 = Colaborador")
    lines.append("(número) = Quantidade de colaborações")
    lines.append("=" * 80)

    return "\n".join(lines)


def create_detailed_structure(heap_data: Dict) -> str:
    """
    Cria uma estrutura detalhada do heap com informações adicionais.
    """
    heap = heap_data["heap"]
    root = heap_data["root"]
    properties = heap_data["properties"]

    lines = []
    lines.append("📋 ESTRUTURA DETALHADA DO HEAP")
    lines.append("=" * 50)
    lines.append("")

    # Informações da raiz
    lines.append("🌳 RAIZ:")
    lines.append(f"   Nome: {root['name']}")
    lines.append(f"   Total de Colaborações: {root['total_collaborations']}")
    lines.append(f"   Colaboradores Únicos: {root['unique_collaborators']}")
    lines.append(f"   Node ID: {root['node_id']}")
    lines.append("")

    # Propriedades do heap
    lines.append("📊 PROPRIEDADES:")
    lines.append(f"   Total de Nós: {properties['total_nodes']}")
    lines.append(f"   Altura do Heap: {properties['heap_height']}")
    lines.append(f"   Máximo de Colaborações: {properties['max_collaborations']}")
    lines.append(f"   Mínimo de Colaborações: {properties['min_collaborations']}")
    lines.append(f"   Média de Colaborações: {properties['avg_collaborations']:.2f}")
    lines.append("")

    # Estrutura hierárquica
    lines.append("🏗️ ESTRUTURA HIERÁRQUICA:")
    lines.append("")

    for i, node in enumerate(heap):
        level = 0
        temp = i
        while temp > 0:
            temp = (temp - 1) // 2
            level += 1

        indent = "  " * level
        arrow = "└─ " if i > 0 else "🌳 "

        if node["is_root"]:
            lines.append(
                f"{indent}{arrow}👑 {node['name']} ({node['collaborations']} colabs)"
            )
        else:
            parent_idx = node["parent_index"]
            parent_name = (
                heap[parent_idx]["name"][:20] + "..."
                if len(heap[parent_idx]["name"]) > 20
                else heap[parent_idx]["name"]
            )
            lines.append(
                f"{indent}{arrow}👤 {node['name']} ({node['collaborations']} colabs) ← filho de {parent_name}"
            )

    return "\n".join(lines)


def create_network_diagram(heap_data: Dict) -> str:
    """
    Cria um diagrama de rede mostrando as conexões.
    """
    heap = heap_data["heap"]

    lines = []
    lines.append("🔗 DIAGRAMA DE REDE DE COLABORAÇÕES")
    lines.append("=" * 50)
    lines.append("")

    # Cria conexões pai-filho
    connections = []
    for i, node in enumerate(heap):
        if i == 0:  # Raiz
            continue

        parent_idx = node["parent_index"]
        parent = heap[parent_idx]

        # Trunca nomes para o diagrama
        parent_name = (
            parent["name"][:15] + "..." if len(parent["name"]) > 15 else parent["name"]
        )
        child_name = (
            node["name"][:15] + "..." if len(node["name"]) > 15 else node["name"]
        )

        connections.append(
            f"{parent_name} ←→ {child_name} ({node['collaborations']} colabs)"
        )

    # Agrupa por nível de colaboração
    high_collab = [c for c in connections if int(c.split("(")[1].split()[0]) >= 10]
    medium_collab = [
        c for c in connections if 5 <= int(c.split("(")[1].split()[0]) < 10
    ]
    low_collab = [c for c in connections if int(c.split("(")[1].split()[0]) < 5]

    if high_collab:
        lines.append("🔥 ALTA COLABORAÇÃO (≥10):")
        for conn in high_collab:
            lines.append(f"   {conn}")
        lines.append("")

    if medium_collab:
        lines.append("⚡ MÉDIA COLABORAÇÃO (5-9):")
        for conn in medium_collab:
            lines.append(f"   {conn}")
        lines.append("")

    if low_collab:
        lines.append("💡 BAIXA COLABORAÇÃO (<5):")
        for conn in low_collab:
            lines.append(f"   {conn}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Função principal."""
    print("🎨 Gerando desenho do heap do professor Yuri...")

    # Carrega os dados
    heap_data = load_heap_data()

    # Cria as representações
    ascii_heap = create_ascii_heap(heap_data)
    detailed_structure = create_detailed_structure(heap_data)
    network_diagram = create_network_diagram(heap_data)

    # Combina tudo
    full_drawing = f"{ascii_heap}\n\n{detailed_structure}\n\n{network_diagram}"

    # Salva o arquivo
    output_file = "data/yuri_heap_drawing.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_drawing)

    print(f"✅ Desenho salvo em: {output_file}")

    # Mostra o desenho no terminal
    print("\n" + "=" * 80)
    print(ascii_heap)
    print("=" * 80)

    print(f"\n📁 Arquivo completo salvo em: {output_file}")


if __name__ == "__main__":
    main()
