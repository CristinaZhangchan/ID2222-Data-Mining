from centrality import GraphDatasetIterator
from typing import Dict, List
import os

#Sort the adjacency list to unify the output format.
#Write the inverted graph to the file inverted_graph.txt in the form of edges to avoid duplication.

# Inverted graph representation
graph: Dict[int, List[int]] = dict()

# Initialize DatasetIterator to read the input file
dataset_iterator = GraphDatasetIterator("web-Google.txt")
max_node_id = 0

# Construct the inverted graph from dataset
for source, target in dataset_iterator:
    source = int(source)
    target = int(target)
    if target not in graph:
        graph[target] = []
    graph[target].append(source)
    max_node_id = max(max_node_id, source, target)

# Sort the adjacency lists for each node
for node in graph.keys():
    graph[node] = sorted(graph[node])

# Write the inverted graph to the output file
with open("inverted_graph.txt", "w") as output_file:
    visited_nodes = set()
    for node in range(max_node_id + 1):
        if node not in graph:
            continue
        if node in visited_nodes:
            continue
        visited_nodes.add(node)
        for neighbor in graph[node]:
            output_file.write(f"{node} {neighbor}{os.linesep}")
        for neighbor in graph[node]:
            if neighbor in graph and neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                for sub_neighbor in graph[neighbor]:
                    output_file.write(f"{neighbor} {sub_neighbor}{os.linesep}")
