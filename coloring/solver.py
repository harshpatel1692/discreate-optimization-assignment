#!/usr/bin/python
# -*- coding: utf-8 -*-
from tqdm import tqdm
import sys


def logic(edges, node_count):

    mapping = dict()
    best_min_colors = node_count
    optimal_colors = []

    for idx in range(node_count):
        mapping[idx] = []

    for i, j in edges:
        mapping[i].append(j)
        mapping[j].append(i)

    priority_of_nodes = list(dict(sorted(mapping.items(), key=lambda e: len(e[1]), reverse=True)).keys())[:10]

    for start_node in tqdm(priority_of_nodes):

        mapping = dict()
        coloring = dict()

        for idx in range(node_count):
            coloring[idx] = list(range(node_count))

        for idx in range(node_count):
            mapping[idx] = []

        for i, j in edges:
            mapping[i].append(j)
            mapping[j].append(i)

        mapping = dict(sorted(mapping.items(), key=lambda e: len(e[1]), reverse=True))

        while len(mapping) > 0:

            coloring[start_node] = coloring[start_node][0]
            connected_nodes = mapping.pop(start_node)

            for j in connected_nodes:

                if coloring[start_node] in coloring[j]:
                    coloring[j].remove(coloring[start_node])

                if start_node in mapping[j]:
                    mapping[j].remove(start_node)

            if mapping:
                mapping = dict(sorted(mapping.items(), key=lambda e: len(e[1]), reverse=True))
                start_node = list(mapping.keys())[0]

        validation_counter = 0
        for i, j in edges:
            status = False if coloring[i] != coloring[j] else True
            if status:
                validation_counter += 1

        if validation_counter == 0 and len(set(coloring.values())) < best_min_colors:
            best_min_colors = len(set(coloring.values()))
            optimal_colors = coloring

    return optimal_colors


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
    output_data = str(len(set(solution.values()))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution.values()))

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

