from collections import defaultdict
from itertools import combinations
from typing import List, Set, Dict
from time import perf_counter

def find_triangles_with_t(graph: Dict[str, Set[str]]) -> int:
    triangles_with_t = 0

    for node, neighbors in graph.items():
        for neighbor1, neighbor2 in combinations(neighbors, 2):
            if neighbor2 in graph[neighbor1]:
                triangle = {node, neighbor1, neighbor2}
                if any(computer.startswith('t') for computer in triangle):
                    triangles_with_t += 1

    return triangles_with_t // 3

def expand_network(graph: Dict[str, Set[str]], node: str) -> Set[str]:
    current_network = {node}
    candidate_nodes = graph[node].copy()

    while candidate_nodes:
        new_network_found = False
        removable_candidates = set()

        for candidate in candidate_nodes.copy():
            if all(candidate in graph[neighbor] for neighbor in current_network):
                current_network.add(candidate)
                candidate_nodes.intersection_update(graph[candidate])
                new_network_found = True
            else:
                removable_candidates.add(candidate)

        candidate_nodes -= removable_candidates

        if not new_network_found:
            break

    return current_network

def find_largest_network(graph: Dict[str, Set[str]]) -> List[str]:
    largest_network = set()

    for node in graph.keys():
        network = expand_network(graph, node)
        if len(network) > len(largest_network):
            largest_network = network

    return sorted(largest_network)

with open('23.input', 'r') as file:
    lines = [line.rstrip('\n') for line in file]
    graph = defaultdict(set)
    for line in lines:
        a, b = line.strip().split("-")
        graph[a].add(b)
        graph[b].add(a)

p1_start = perf_counter()
count_with_t = find_triangles_with_t(graph)
print(f"Part One: {count_with_t}")
p1_end = perf_counter()

p2_start = perf_counter()
largest_network = find_largest_network(graph)
password = ",".join(largest_network)
print(f"Part Two: {password}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")