#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import statistics

Item = namedtuple("Item", ['index', 'value', 'weight', 'value_per_weight'])


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

    # We want at least 1 of the top 1% precious items in the knapsack
    max_threshold = int(total_items*0.20) if total_items >= 1000 else total_items

    # sort the values by Value in descending order
    sorted_values = sorted(items, key=lambda x: x.value, reverse=True)[:max_threshold]

    # For remainder items, we only want items that has value per weight more than 0.5
    threshold_v_w = statistics.quantiles([item.value_per_weight for item in items], n=10)

    items_v_w = []

    for idx, value in enumerate(threshold_v_w):
        if idx == 0:
            temp_list = [item for item in items if 0 < item.value_per_weight <= value]
            # temp_threshold = statistics.mean([item.value_per_weight for item in temp_list])
            # items_v_w += [item for item in items if item.value_per_weight >= temp_threshold]
            temp_list = sorted(temp_list, key=lambda x: x.value_per_weight, reverse=True)
            items_v_w = temp_list[:int(len(temp_list)*0.5)]

        elif idx == len(threshold_v_w)-1:
            temp_list = [item for item in items if item.value_per_weight > value]
            # temp_threshold = statistics.mean([item.value_per_weight for item in temp_list])
            # items_v_w += [item for item in items if item.value_per_weight >= temp_threshold]
            temp_list = sorted(temp_list, key=lambda x: x.value_per_weight, reverse=True)
            items_v_w = temp_list[:int(len(temp_list)*0.5)]
        else:
            temp_list = [item for item in items if value < item.value_per_weight <= threshold_v_w[idx+1]]
            # temp_threshold = statistics.mean([item.value_per_weight for item in temp_list])
            # items_v_w += [item for item in items if item.value_per_weight >= temp_threshold]
            temp_list = sorted(temp_list, key=lambda x: x.value_per_weight, reverse=True)
            items_v_w = temp_list[:int(len(temp_list)*0.5)]

    # Sort the values by weight in descending order
    if total_items > 1000:
        sorted_v_w = sorted(items_v_w, key=lambda x: x.value_per_weight, reverse=True)
    else:
        sorted_v_w = sorted(items, key=lambda x: x.value_per_weight, reverse=True)

    for first_item in sorted_values:

        for idx in range(len(sorted_v_w)):

            # Empty knapsack
            temp_idx = []

            # Load first item in the knapsack
            temp_value = first_item.value
            temp_weight = first_item.weight
            temp_idx.append(first_item.index)

            for next_item in sorted_v_w[idx:]:

                # Ignore the item that is already picked
                if first_item.index == next_item.index:
                    continue

                # If current weight + next weight exceeds capacity then ignore and try another
                if temp_weight + next_item.weight > capacity:
                    continue

                temp_value += next_item.value
                temp_weight += next_item.weight
                temp_idx.append(next_item.index)

            # If current solution is more valuable than previous solutions; then use the current mix of items.
            if temp_value > value and temp_weight <= capacity:
                value = temp_value
                taken_idx = temp_idx

    # Flag the items that were taken to yield max value
    taken = [0]*total_items
    for idx in taken_idx:
        taken[idx] = 1

    return value, taken


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
    value, taken = logic(items, capacity)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

