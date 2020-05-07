#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import time
from collections import namedtuple, defaultdict
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp

Set = namedtuple("Set", ['index', 'cost', 'items'])

# You need to subclass the cp_model.CpSolverSolutionCallback class.
class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.start = time.time()
        self.start_interval = time.time()

    def on_solution_callback(self):
        t1 = time.time()
        time_used = t1 - self.start
        interval_used = t1 - self.start_interval
        self.start_interval = t1
        print('Interval using %.4f, Accu using %.4f, Solution %i' % (interval_used, time_used, self.__solution_count), end = ', ')
        print('objective value = %i' % self.ObjectiveValue())
        #for v in self.__variables:
        #    print('  %s = %i' % (v, self.Value(v)), end=',')
        #print()
        self.__solution_count += 1

    def solution_count(self):
        return self.__solution_count

def mip_solver(sets, set_count, item_count):
    'solve the simple mip of linear relaxation problem and return solution'
    solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    have_item = np.zeros([set_count, item_count], dtype='int')
    cost = [int(s.cost) for s in sets]
    x = [solver.NumVar(0, 1, "x%d" %i) for i in range(set_count)]
    
    for s in range(set_count):
        for i in sets[s].items:
            have_item[s,i] = 1

    for i in range(item_count):
        solver.Add(sum(have_item[s][i]*x[s] for s in range(set_count)) >= 1)

    solver.Minimize(sum(cost[s]*x[s] for s in range(set_count)))

    solution = [0]*set_count
    obj = solver.Objective().Value()
    for idx, xi in enumerate(x):
        solution[idx] = xi.solution_value()

    return solution, obj

def cp_solver(sets, set_count, item_count, max_minutes=10):
    set_range = range(set_count)
    item_range = range(item_count)
    have_item = np.zeros([set_count, item_count], dtype='int')
    cost = [int(s.cost) for s in sets]
    max_cost = sum(cost)

    # create model
    model = cp_model.CpModel()

    # create the variables
    x = [0]*set_count
    for s in set_range:
        for i in sets[s].items:
            have_item[s,i] = 1
    for s in set_range:
        x[s] = model.NewBoolVar('x%s'%(s))
    
    # create the constraints
    for i in item_range:
        model.Add(sum(have_item[s][i]*x[s] for s in set_range) >= 1)
    
    # create the objective
    model.Minimize(sum(cost[s]*x[s] for s in set_range))

    # create a solver and solves
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    solver.parameters.max_time_in_seconds = 60*max_minutes
    solution_printer = VarArrayAndObjectiveSolutionPrinter(x)
    status = solver.SolveWithSolutionCallback(model, solution_printer)
    print('----------------')
    print('Status       : %s' % solver.StatusName(status))
    print('#sol found   : %i' % solution_printer.solution_count())
    print('Branches     : %i' % solver.NumBranches())
    print('Wall time    : %f s' % solver.WallTime())


    solution = [0]*set_count

    obj = solver.ObjectiveValue()
    for idx, xi in enumerate(x):
        solution[idx] = solver.Value(xi)
    
    return solution, obj


def greedy_1(sets, set_count, item_count):
    solution = [0]*set_count
    coverted = set()

    sorted_sets = sorted(sets, key=lambda s: s.cost/len(s.items) if len(s.items) > 0 else s.cost)

    for s in sorted_sets:
        solution[s.index] = 1
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break
    
    # calculate the cost of the solution
    obj = sum([s.cost*solution[s.index] for s in sets])

    return solution, obj

def greedy_2(sets, set_count, item_count):
    solution = [0]*set_count
    covered = set()
    
    while len(covered) < item_count:
        sorted_sets = sorted(sets, key=lambda s: -s.cost*len(set(s.items)-covered) if len(set(s.items)-covered) > 0 else s.cost)
        for s in sorted_sets:
            if solution[s.index] < 1:
                solution[s.index] = 1
                covered |= set(s.items)
                break
        
        obj = sum([s.cost*solution[s.index] for s in sets])
    
    return solution, obj

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), list(map(int, parts[1:]))))

    # build a trivial solution
    # pick add sets one-by-one until all the items are covered
    

    # solution, obj = greedy_1(sets, set_count, item_count)
    # solution, obj = greedy_2(sets, set_count, item_count)
    # solution, obj = cp_solver(sets, set_count, item_count, max_minutes=1)
    solution, obj = mip_solver(sets, set_count, item_count)
    # for s in sets:
    #     solution[s.index] = 1
    #     coverted |= set(s.items)
    #     if len(coverted) >= item_count:
    #         break
        
    # calculate the cost of the solution
    obj = sum([s.cost*solution[s.index] for s in sets])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')