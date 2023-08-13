#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import heapq
from heapq import heappop, heappush
from tqdm import tqdm
import statistics

Item = namedtuple("Item", ['index', 'value', 'weight', 'value_per_weight'])
Node = namedtuple("Node", ['direction', 'index', 'branch', 'value', 'weight', 'estimate'])


def get_children(node_value, capacity, node_estimate, items, branch):

    if branch > len(items):
        return None, None

    item = items[branch-1]

    if capacity-item.weight >= 0 :
        left_node = Node('left', item.index, branch, node_value+item.value, capacity-item.weight, node_estimate)
        right_node = Node('right', item.index, branch, node_value, capacity, node_estimate-item.value)
    else:
        left_node = Node('left', item.index, branch, -1, capacity-item.weight, -1)
        right_node = Node('right', item.index, branch, node_value, capacity, node_estimate-item.value)

    return left_node, right_node, branch


def logic(items, capacity):
    """
    - We want at least 1 of the valuable item in the knapsack to be from top 20% of the most valuable items.
    - First value in the knapsack will be the one with the highest value.
    - Remainder of the values will be filled in the order of max value per weight.
    - For remainder items, we want item with value per weight ratio more than mean value of items present per decile.
    - Iterate through all the cases and use the items that yield max value.

    :param items: List of tuple
    :param capacity: Max value that a knapsack can fit
    :return: Total value of the knapsack;
    """

    value = 0
    taken_idx = []
    total_items = len(items)
    total_value = sum([item.value for item in items])

    # sort by value by weight in descending order
    items = sorted(items, key=lambda x: x.value, reverse=True)

    unexplored_nodes = []
    max_value = 0

    # First Branch
    left_node, right_node, current_branch = get_children(0, capacity, total_value, items, 1)
    unexplored_nodes.append(left_node)
    unexplored_nodes.append(right_node)
    unexplored_nodes = sorted(unexplored_nodes, key=lambda x: x.estimate)

    counter = 0

    while True:

        explore_node = unexplored_nodes.pop()

        left_node, right_node, current_branch = get_children(explore_node.value, explore_node.weight, explore_node.estimate, items, explore_node.branch+1)

        if current_branch != total_items:

            if left_node.estimate > max_value:
                unexplored_nodes.append(left_node)

            if right_node.estimate > max_value:
                unexplored_nodes.append(right_node)
        else:
            if left_node.estimate > right_node.estimate and left_node.estimate > max_value:
                max_value = left_node.estimate

            elif right_node.estimate > left_node.estimate and right_node.estimate > max_value:
                max_value = right_node.estimate

        filtered_nodes = [node for node in unexplored_nodes if node.estimate > max_value]

        unexplored_nodes = sorted(filtered_nodes, key=lambda x: x.estimate)

        if not unexplored_nodes:
            break
        else:
            counter += 1

    print(counter, max_value)
    # return max_value

    # # Flag the items that were taken to yield max value
    # taken = [0]*total_items
    # for idx in taken_idx:
    #     taken[idx] = 1
    #
    # print(sum(taken))
    # return value, taken


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0])/int(parts[1])))

    # Fill knapsack
    logic(items, capacity)

    # value, taken = logic(items, capacity)

    # # prepare the solution in the specified output format
    # output_data = str(value) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, taken))
    # return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

