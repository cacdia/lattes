#!/usr/bin/env python3
"""
Script para criar uma estrutura de heap com o professor Yuri como raiz,
organizando colaboradores por quantidade de colaborações.
"""

import json
import uuid
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import heapq


def load_publications_data() -> List[Dict]:
    """Carrega os dados de publicações unificadas."""
    with open("data/publicacoes_unificadas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def find_yuri_collaborations(publications: List[Dict]) -> Dict[str, int]:
    """
    Encontra todas as colaborações do Yuri com outros professores.
    Retorna um dicionário com nome do colaborador e quantidade de colaborações.
    """
    yuri_collaborations = defaultdict(int)

    for pub in publications:
        professores = pub.get("professores", [])

        # Verifica se Yuri está na publicação
        if "Yuri de Almeida Malheiros Barbosa" in professores:
            # Conta colaborações com outros professores
            for prof in professores:
                if prof != "Yuri de Almeida Malheiros Barbosa":
                    yuri_collaborations[prof] += 1

    return dict(yuri_collaborations)


def create_heap_structure(collaborations: Dict[str, int]) -> Dict:
    """
    Cria uma estrutura de heap com Yuri como raiz.
    Organiza colaboradores por quantidade de colaborações (max-heap).
    """
    # Converte para lista de tuplas (peso, nome) para usar com heapq
    # Usamos peso negativo para criar um max-heap
    heap_items = [(-count, name) for name, count in collaborations.items()]
    heapq.heapify(heap_items)

    # Estrutura do heap
    heap_structure = {
        "root": {
            "name": "Yuri de Almeida Malheiros Barbosa",
            "total_collaborations": sum(collaborations.values()),
            "unique_collaborators": len(collaborations),
            "node_id": str(uuid.uuid4()),
        },
        "heap": [],
        "collaborators": [],
    }

    # Constrói o heap
    heap_array = []
    collaborators_list = []

    # Adiciona Yuri como raiz (índice 0)
    heap_array.append(
        {
            "index": 0,
            "name": "Yuri de Almeida Malheiros Barbosa",
            "collaborations": sum(collaborations.values()),
            "node_id": heap_structure["root"]["node_id"],
            "is_root": True,
        }
    )

    # Adiciona colaboradores ordenados por quantidade de colaborações
    index = 1
    while heap_items:
        neg_count, name = heapq.heappop(heap_items)
        count = -neg_count

        node = {
            "index": index,
            "name": name,
            "collaborations": count,
            "node_id": str(uuid.uuid4()),
            "is_root": False,
            "parent_index": (index - 1) // 2 if index > 0 else 0,
        }

        heap_array.append(node)
        collaborators_list.append(
            {
                "name": name,
                "collaborations_with_yuri": count,
                "node_id": node["node_id"],
            }
        )

        index += 1

    heap_structure["heap"] = heap_array
    heap_structure["collaborators"] = collaborators_list

    return heap_structure


def calculate_heap_properties(heap_structure: Dict) -> Dict:
    """
    Calcula propriedades adicionais do heap para análise.
    """
    heap = heap_structure["heap"]
    collaborators = heap_structure["collaborators"]

    if not collaborators:
        return {
            "total_nodes": 1,
            "max_collaborations": 0,
            "min_collaborations": 0,
            "avg_collaborations": 0,
            "heap_height": 0,
        }

    collaboration_counts = [c["collaborations_with_yuri"] for c in collaborators]

    return {
        "total_nodes": len(heap),
        "max_collaborations": max(collaboration_counts),
        "min_collaborations": min(collaboration_counts),
        "avg_collaborations": sum(collaboration_counts) / len(collaboration_counts),
        "heap_height": len(bin(len(heap))) - 2,  # Altura aproximada do heap
    }


def main():
    """Função principal."""
    print("🔍 Carregando dados de publicações...")
    publications = load_publications_data()

    print("📊 Analisando colaborações do Yuri...")
    collaborations = find_yuri_collaborations(publications)

    print(f"✅ Encontradas {len(collaborations)} colaborações únicas")
    print(f"📈 Total de colaborações: {sum(collaborations.values())}")

    print("🌳 Criando estrutura de heap...")
    heap_structure = create_heap_structure(collaborations)

    print("📐 Calculando propriedades do heap...")
    properties = calculate_heap_properties(heap_structure)
    heap_structure["properties"] = properties

    # Salva o arquivo
    output_file = "data/professor_yuri_heap.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(heap_structure, f, ensure_ascii=False, indent=2)

    print(f"💾 Arquivo salvo em: {output_file}")

    # Mostra estatísticas
    print("\n📊 Estatísticas do Heap:")
    print(f"   • Total de nós: {properties['total_nodes']}")
    print(f"   • Altura do heap: {properties['heap_height']}")
    print(f"   • Máximo de colaborações: {properties['max_collaborations']}")
    print(f"   • Mínimo de colaborações: {properties['min_collaborations']}")
    print(f"   • Média de colaborações: {properties['avg_collaborations']:.2f}")

    # Mostra top 5 colaboradores
    print("\n🏆 Top 5 Colaboradores:")
    top_collaborators = sorted(
        collaborations.items(), key=lambda x: x[1], reverse=True
    )[:5]
    for i, (name, count) in enumerate(top_collaborators, 1):
        print(f"   {i}. {name}: {count} colaborações")


if __name__ == "__main__":
    main()
