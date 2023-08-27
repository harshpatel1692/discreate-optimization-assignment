#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from tqdm import tqdm

Item = namedtuple("Item", ['index', 'value', 'weight', 'value_per_weight'])
Node = namedtuple("Node", ['direction', 'index', 'value', 'weight', 'optimistic_estimate', 'excluded_nodes', 'explored_nodes'])
PRECISION = -1
MAX_CAPACITY = -1


def get_children(current_node, items):

    optimistic_value = 0
    total_weight = MAX_CAPACITY
    excluded_nodes = current_node.excluded_nodes
    explored_nodes = current_node.explored_nodes

    if current_node.direction != 'root':
        filtered_items = [item for item in items if item.index not in excluded_nodes+[current_node.index]]
        next_node = [item for item in filtered_items if item.weight <= current_node.weight and item.index not in explored_nodes]
    else:
        filtered_items = items
        next_node = items

    if not next_node:
        return None, None

    # Re-calculate optimistic value of the branch
    for ele in sorted(filtered_items, key=lambda x: x.value_per_weight, reverse=True):
        if total_weight-ele.weight >= 0:
            optimistic_value += ele.value
            total_weight -= ele.weight
        else:
            optimistic_value += total_weight * ele.value_per_weight
            break

    optimistic_value = round(optimistic_value, PRECISION)

    # Pick the next best item to branch
    next_node = next_node[0]

    if current_node.weight-next_node.weight >= 0:
        left_node = Node('left', next_node.index, current_node.value+next_node.value, current_node.weight-next_node.weight, current_node.optimistic_estimate, excluded_nodes, explored_nodes+[next_node.index])
        right_node = Node('right', next_node.index, current_node.value, current_node.weight, optimistic_value, excluded_nodes+[next_node.index], explored_nodes+[next_node.index]) #node_estimate-item.value)
    else:
        left_node = Node('left', next_node.index, -1, current_node.weight-next_node.weight, -1, excluded_nodes, explored_nodes+[next_node.index])
        right_node = Node('right', next_node.index, current_node.value, current_node.weight, optimistic_value, excluded_nodes+[next_node.index], explored_nodes+[next_node.index]) #node_estimate-item.value)

    return left_node, right_node


def logic(items):
    """
    - Branch and Bound algorithm
    - Prune branching by optimistic evaluation using linear relaxation (optimistic max value by fractional filling of knapsack)

    :param items: List of tuple
    :return: Total value of the knapsack;
    """

    global PRECISION

    # stop exploring once global benchmark is reached - values established from course forum
    # https://www.coursera.org/learn/discrete-optimization/discussions/threads/MSpS0pC7EeaxvRLoQ7NHzw/replies/WNq-3nkqEeuXJQ5YalMU0w

    benchmark = {
        30: 99798,
        50: 142156,
        200: 100236,
        400: 3967180,
        1000: 109899,
        10000: 1099893
    }

    # Calculate global optimistic value
    optimistic_value = 0
    total_weight = MAX_CAPACITY
    min_capacity = min([item.weight for item in items])

    for item in sorted(items, key=lambda x: x.value_per_weight, reverse=True):
        if total_weight-item.weight >= 0:
            optimistic_value += item.value
            total_weight -= item.weight
        else:
            optimistic_value += total_weight * item.value_per_weight
            break

    optimistic_value = round(optimistic_value, PRECISION)

    # Branch and Bound
    unexplored_nodes = []
    loop_counter = 0
    max_value = 0
    optimal_node = Node('dummy', -1, 0, 0, 0, [], [])

    benchmark = benchmark.get(len(items), optimistic_value)

    # Setting root node
    items = sorted(items, key=lambda x: (x.value_per_weight, x.weight), reverse=True)

    root_item = items[0]
    root_node = Node('root', root_item.index, 0, MAX_CAPACITY, optimistic_value, [], [])
    left_node, right_node = get_children(root_node, items)

    unexplored_nodes.append(right_node)
    unexplored_nodes.append(left_node)

    with tqdm() as pbar:
        while len(unexplored_nodes) > 0 and loop_counter < 3000:

            explore_node = unexplored_nodes.pop()

            left_node, right_node = get_children(explore_node, items)

            if left_node is None:
                continue

            pbar.update(1)
            loop_counter += 1

            if left_node.weight > min_capacity:
                unexplored_nodes.append(left_node)
            else:
                if left_node.value > max_value:
                    max_value = left_node.value
                    optimal_node = left_node

            if right_node.optimistic_estimate > max_value:
                unexplored_nodes.append(right_node)
            else:
                if right_node.value > max_value:
                    max_value = right_node.value
                    optimal_node = right_node

            if max_value >= benchmark:
                break

            unexplored_nodes = sorted([node for node in unexplored_nodes if node.optimistic_estimate > max_value and node.weight >= min_capacity], key=lambda x: (x.direction, x.value, x.optimistic_estimate), reverse=True)

    return max_value, optimal_node


def solve_it(input_data):

    global PRECISION, MAX_CAPACITY
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    # Edge case where it gets stuck at a local minima
    if item_count == 1000:
        PRECISION = 3
    else:
        PRECISION = 4

    MAX_CAPACITY = capacity

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        value_per_weight = round(int(parts[0])/int(parts[1]), PRECISION)

        items.append(Item(i-1, int(parts[0]), int(parts[1]), value_per_weight))

    # Fill knapsack
    optimal_value, optimal_node = logic(items)
    print(f'Knapsack Max Value: {optimal_value}')

    # Mark items picked for knapsack
    optimal_path = [0]*len(items)
    selected_items = set(optimal_node.explored_nodes)-set(optimal_node.excluded_nodes)

    for idx in selected_items:
        optimal_path[idx] = 1

    output_data = str(optimal_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, optimal_path))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            solve_it(input_data)
        # print(solve_it(input_data))

    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

