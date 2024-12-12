from hyperloglog import HyperLogLog
from typing import Dict, Tuple, List
from collections import defaultdict
import os

# Probabilistic cardinality counters for all vertices
vertex_counters: Dict[str, HyperLogLog] = dict()
iteration_stats: Dict[Tuple[str, int], int] = dict()


class GraphDatasetIterator:
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        self.file_descriptor = open(self.file_path, "r")
        return self

    def __del__(self):
        self.file_descriptor.close()

    def __next__(self):
        while True:
            line = self.file_descriptor.readline()
            if len(line) == 0:
                raise StopIteration
            if line.startswith("#"):
                continue
            data = line.strip().split()
            return data[0], data[1]


def save_checkpoint(stats, iteration):
    with open("iteration_stats.txt", "a") as f:
        for key in vertex_counters.keys():
            f.write(f"{key} {iteration} {stats[(key, iteration)]}{os.linesep}")
        f.write("====" + os.linesep)


# Centrality computation using distance to nodes
if __name__ == "__main__":
    dataset_iterator = GraphDatasetIterator("inverted_graph.txt")
    last_node = None
    count = 0

    # Initialize probabilistic counters for each node
    for target, source in dataset_iterator:
        if target not in vertex_counters:
            vertex_counters[target] = HyperLogLog()
            vertex_counters[target].add(target)
            iteration_stats[(target, 0)] = 1
            iteration_stats[(target, 1)] = 0
        if source not in vertex_counters:
            vertex_counters[source] = HyperLogLog()
            vertex_counters[source].add(source)
            iteration_stats[(source, 0)] = 1
            iteration_stats[(source, 1)] = 0
        if target != last_node:
            if last_node is not None:
                iteration_stats[(last_node, 0)] = 0
                iteration_stats[(last_node, 1)] = count
            last_node = target
            count = 1
        else:
            count += 1
        vertex_counters[target].add(source)

    if last_node is not None:
        iteration_stats[(last_node, 0)] = 0
        iteration_stats[(last_node, 1)] = count

    save_checkpoint(iteration_stats, 0)
    save_checkpoint(iteration_stats, 1)

    iteration = 2
    while True:
        print("Iteration: ", iteration)

        dataset_iterator = GraphDatasetIterator("inverted_graph.txt")
        temp_vertex_counters: Dict[str, HyperLogLog] = dict()
        last_node = None
        # Iterate through dataset to update temporary counters
        for target, source in dataset_iterator:
            if target not in temp_vertex_counters:
                temp_vertex_counters[target] = vertex_counters[target]
            if source not in temp_vertex_counters:
                temp_vertex_counters[source] = vertex_counters[source]
            # Merge the current source counter into the target counter
            #Updates are stored in temporary counters (temp_vertex_counters) to
            #  avoid overwriting current values during iteration.
            temp_vertex_counters[target].merge(vertex_counters[source])

        changed = False
        delta = 0.0

        # Update probabilistic counters for each node
        for key in vertex_counters.keys():
            vertex_counters[key] = temp_vertex_counters[key]
            iteration_stats[(key, iteration)] = vertex_counters[key].estimate_cardinality()
            delta += iteration_stats[(key, iteration)] - iteration_stats[(key, iteration - 1)]
            if iteration_stats[(key, iteration)] != iteration_stats[(key, iteration - 1)]:
                changed = True

        print("Delta: ", delta)

        save_checkpoint(iteration_stats, iteration)

        # Terminate if no changes or iteration exceeds limit
        if not changed or iteration > 15:
            break

        iteration += 1

    print()
    print("Calculating harmonic centrality")
    harmonic_centrality: Dict[str, float] = defaultdict(int)
    total_nodes = len(vertex_counters)
    
    #harmonic centrality calculation
    for i in range(1, iteration + 1):
        for node in vertex_counters.keys():
            harmonic_centrality[node] += (iteration_stats[(node, iteration)] - iteration_stats[(node, iteration - 1)]) / iteration
    #将节点按谐波中心性降序排列，并输出中心性最高和最低的节点
    sorted_centrality = sorted(list(map(lambda x: (x[1], x[0]), harmonic_centrality.items())), reverse=True)

    top_n = 5
    print(f"===== Top {top_n}: {sorted_centrality[:top_n]}")
    for value, node in sorted_centrality[:top_n]:
        print(f"Node: {node}")
        for rnd in range(1, iteration + 1):
            print(f"    Iteration: {rnd} Cardinality: {iteration_stats[(node, rnd)]}")

    bottom_n = 5
    print(f"===== Bottom {bottom_n}: {sorted_centrality[-bottom_n:]}")
    for value, node in sorted_centrality[-bottom_n:]:
        print(f"Node: {node}")
        for rnd in range(1, iteration + 1):
            print(f"    Iteration: {rnd} Cardinality: {iteration_stats[(node, rnd)]}")
