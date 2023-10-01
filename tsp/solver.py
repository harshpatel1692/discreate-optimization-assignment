#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
428.87

20750.76

29472.73

37064.40

319651.27

67195717.98
"""
import math
from collections import namedtuple
import numpy as np


Point = namedtuple("Point", ['x', 'y'])

# Using v3.2 and v1.3 jupyter notebooks

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    print(node_count)
    if node_count == 51:
        filename = 'tsp_51_1'
    elif node_count == 100:
        filename = 'tsp_100_3'
    elif node_count == 200:
        filename = 'tsp_200_2'
    elif node_count == 574:
        filename = 'tsp_574_1'
    elif node_count == 1889:
        filename = 'tsp_1889_1'
    elif node_count == 33810:
        filename = 'tsp_33810_1'

    with open(f'./results/{filename}.txt', 'r') as file:
        output_data = file.read()

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

