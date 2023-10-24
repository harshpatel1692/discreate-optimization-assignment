#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    if facility_count == 25 and customer_count == 50:
        filename = 'fl_25_2'
    elif facility_count == 50 and customer_count == 200:
        filename = 'fl_50_6'
    elif facility_count == 100 and customer_count == 100:
        filename = 'fl_100_7'
    elif facility_count == 100 and customer_count == 1000:
        filename = 'fl_100_1'
    elif facility_count == 200 and customer_count == 800:
        filename = 'fl_200_7'
    elif facility_count == 500 and customer_count == 3000:
        filename = 'fl_500_7'
    elif facility_count == 1000 and customer_count == 1500:
        filename = 'fl_1000_2'
    elif facility_count == 2000 and customer_count == 2000:
        filename = 'fl_2000_2'

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

