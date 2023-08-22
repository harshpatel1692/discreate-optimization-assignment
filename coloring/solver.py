#!/usr/bin/python
# -*- coding: utf-8 -*-
from tqdm import tqdm
import sys


def logic(edges, node_count):

    mapping = dict()
    coloring = dict()
    colors_available = dict()

    for idx in range(node_count):
        coloring[idx] = 0

    for idx in range(node_count):
        colors_available[idx] = list(range(node_count))

    for idx in range(node_count):
        mapping[idx] = []

    for i, j in edges:
        mapping[i].append(j)
        mapping[j].append(i)

    mapping = dict(sorted(mapping.items(), key=lambda e: len(e[1]), reverse=True))

    for start_node in tqdm(mapping):

        colors_available[start_node] = colors_available[start_node][0]

        for j in mapping[start_node]:

            if colors_available[j][0] == colors_available[start_node]:
                colors_available[j].remove(colors_available[start_node])

            if start_node in mapping[j]:
                mapping[j].remove(start_node)

    return colors_available


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

