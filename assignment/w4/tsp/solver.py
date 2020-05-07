#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import functools
import copy

Point = namedtuple("Point", ['x', 'y'])
Cost = namedtuple("Cost", ["subset", 'dest', 'min'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def get_subsets(s):
    n = len(s)
    subsets = [[] for i in range(n+1)]
    
    for i in range(1 << (n-1), 1 << n):
        subset = [s[bit] for bit in range(n) if is_bit_set(i, bit, n)]
        subsets[len(subset)].append(subset)
    
    return subsets

def is_bit_set(num, bit, n):
    return num & (1 << (n-1-bit)) > 0

def bitsmap(subset):
    sum = 0
    for sub in subset:
        sum = sum + (1 << sub)
    return sum

def min_distance(C, points, subset, j):
    min_dis = sys.maxsize
    index = -1
    for i in subset:
        if i == j:
            continue
        temp = C[bitsmap(subset) - (1 << j)][i]['value'] + length(points[i], points[j])

        if temp < min_dis:
            min_dis = temp
            index = i
    
    return min_dis, index
def dynamic_programming(nodeCount, points):
    subsets = get_subsets(range(0, nodeCount))
    C = {}
    order = []
    C[1<<0] = {0 : {'value': 0, 'index': 0}}
    for s in range(2, nodeCount + 1):
        for subset in subsets[s]:
            C[bitsmap(subset)] = {0 : {'value': sys.maxsize, 'index': -1}}
            for j in subset:
                if j == 0:
                    continue
                # min_dis = min(C[bitsmap(subset) - (1 << j)][i] + length(points[i], points[j]) for i in subset if i != j)
                min_dis, index = min_distance(C, points, subset, j)
                C[bitsmap(subset)][j] = {'value': min_dis, 'index': index}

    for j in subsets[-1][0]:
        min_dis = sys.maxsize
        index = -1
        if j == 0: 
            continue
        temp = C[bitsmap(subsets[-1][0])][j]['value'] + length(points[j], points[0])
        if temp < min_dis:
            min_dis = temp
            index = j
    
    # print(index)
    # order.append(0)
    order.append(index)
    subset = copy.copy(subsets[-1][0])
    # print(subset.remove(4))
    # subset.remove(0)
    # print(subset)
    for _ in range(nodeCount-2):
        # print(C[bitsmap(subset)])
        id = index
        index = C[bitsmap(subset)][index]['index']

        order.append(index)
        subset.remove(id)
        # print(subset)
        if len(subset) == 2:
            break
    order.append(0)
    order.reverse()
    # print(order)

    return min_dis, order


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    # cityList = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
        # cityList.append(City(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)
    # subsets = get_subsets(solution)
    
    # min, solution = dynamic_programming(nodeCount, points)
    # geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
