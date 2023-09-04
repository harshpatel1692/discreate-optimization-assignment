#!/usr/bin/python
# -*- coding: utf-8 -*-
from tqdm import tqdm
import sys
import random
from collections import Counter
from copy import deepcopy


class TabuList:
    def __init__(self, tabu_size):
        self.tabu_size = tabu_size
        self.tabu_hash = set()
        self.tabu_queue = []

    def is_present(self, node):
        return node in self.tabu_hash

    def insert(self, node):
        if self.is_present(node):
            return
        self.tabu_hash.add(node)
        self.tabu_queue.append(node)
        if len(self.tabu_hash) > self.tabu_size:
            self.remove()

    def remove(self):
        top = self.tabu_queue.pop(0)
        self.tabu_hash.remove(top)


def get_conflicts(graph, coloring):

    node_count = len(graph)
    conflicts = [0 for _ in range(node_count)]

    for node, neighbors in enumerate(graph):
        for neighbor in neighbors:
            if coloring[node] == coloring[neighbor]:
                conflicts[node] += 1

    return conflicts


def max_violation_node(conflict_mapping, tabu_list):

    max_conflicts = max([conflict for node, conflict in enumerate(conflict_mapping) if not tabu_list.is_present(node)])

    if max_conflicts == 0:
        return -1

    # Create a new dictionary with only the key-value pairs that have the maximum value and not in tabu list
    max_conflict_nodes = [node for node, conflict in enumerate(conflict_mapping) if conflict == max_conflicts and not tabu_list.is_present(node)]

    if not max_conflict_nodes:
        return -1

    return random.choice(max_conflict_nodes)


def remove_color(coloring, max_colors):

    pick_color = random.randint(0, max_colors-1)

    new_coloring = []

    for c in coloring:
        if c == pick_color:
            new_coloring.append(random.randint(0, max_colors-2))
        elif c > pick_color:
            new_coloring.append(c-1)
        else:
            new_coloring.append(c)

    return new_coloring


def unfamous_color(node, graph, coloring, max_colors):

    node_color = coloring[node]
    neighbor_colors = [coloring[color] for color in graph[node]]
    color_count = Counter(neighbor_colors)

    min_color = min([v for k, v in color_count.items() if k != node_color])

    unused_colors = list(set(range(max_colors))-set(color_count.keys()))

    if unused_colors:
        return random.choice(unused_colors)
    else:
        least_colors = [k for k, v in color_count.items() if v == min_color and k != node_color]
        return random.choice(least_colors)


def check_feasibility(graph, coloring, max_colors, tabu_limit):
    max_iterations = 50000
    iteration = 0
    conflicts = get_conflicts(graph, coloring)
    total_conflicts = sum(conflicts)
    tabu_list = TabuList(tabu_limit)

    while iteration < max_iterations and total_conflicts > 0:

        node = max_violation_node(conflicts, tabu_list)

        while node == -1:
            tabu_list.remove()
            node = max_violation_node(conflicts, tabu_list)

        tabu_list.insert(node)
        least_used_color = unfamous_color(node, graph, coloring, max_colors)

        for neighbor in graph[node]:
            if coloring[neighbor] == coloring[node]:
                conflicts[neighbor] -= 1
                conflicts[node] -= 1
            elif coloring[neighbor] == least_used_color:
                conflicts[neighbor] += 1
                conflicts[node] += 1

        coloring[node] = least_used_color

        # conflicts = get_conflicts(graph, coloring)
        total_conflicts = sum(conflicts)

        iteration += 1

    return sum(conflicts) == 0, coloring, conflicts, iteration


def get_suboptimal_coloring(mapping):

    mapping = deepcopy(mapping)

    node_count = len(mapping)
    coloring = [[] for _ in range(node_count)]

    for idx in range(node_count):
        coloring[idx] = list(range(node_count))

    for start_node in range(node_count):

        if isinstance(coloring[start_node], list):
            coloring[start_node] = coloring[start_node][0]
        else:
            continue

        for j in mapping[start_node]:

            if coloring[start_node] in coloring[j]:
                coloring[j].remove(coloring[start_node])

            if start_node in mapping[j]:
                mapping[j].remove(start_node)

    del mapping
    return coloring


def logic(edges, node_count):

    tabu_limit = node_count // 10

    mapping = [[] for _ in range(node_count)]

    for i, j in edges:
        mapping[i].append(j)
        mapping[j].append(i)

    new_coloring = get_suboptimal_coloring(mapping) #[random.randint(0, max_color-1) for _ in range(node_count)]
    max_color = len(set(new_coloring))

    max_retries = tabu_limit
    retry = max_retries

    while retry > 0:

        is_feasible, coloring, conflicts, iteration = check_feasibility(mapping, new_coloring, max_color, tabu_limit)

        if is_feasible:
            max_color -= 1
            optimal_coloring = deepcopy(coloring)
            retry = max_retries

        else:
            retry -= 1

        new_coloring = remove_color(optimal_coloring, max_color)

    print(max_color, is_feasible, len(set(coloring)), sum(conflicts), iteration)

    return optimal_coloring


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    solution = logic(edges, node_count)

    # prepare the solution in the specified output format
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

