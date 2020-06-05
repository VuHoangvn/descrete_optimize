# #!/usr/bin/python
# # -*- coding: utf-8 -*-

# from collections import namedtuple
# import math
# from datetime import datetime
# import numpy
# from ortools.linear_solver import pywraplp

# Point = namedtuple("Point", ['x', 'y'])
# Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
# Customer = namedtuple("Customer", ['index', 'demand', 'location'])

# def length(point1, point2):
#     return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# def solve_it(input_data):
#     # Modify this code to run your optimization algorithm

#     # parse the input
#     lines = input_data.split('\n')

#     parts = lines[0].split()
#     facility_count = int(parts[0])
#     customer_count = int(parts[1])
    
#     facilities = []
#     for i in range(1, facility_count+1):
#         parts = lines[i].split()
#         facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

#     customers = []
#     for i in range(facility_count+1, facility_count+1+customer_count):
#         parts = lines[i].split()
#         customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

#     obj, solution = ortools_solve(facilities, customers)

#     print('Solution got at {}'.format(datetime.now().time()))
#     # prepare the solution in the specified output format
#     output_data = '%.2f' % obj + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, solution))

#     return output_data




# def ortools_solve(facilities, customers, time_limit=None):
#     # print('Num facilities {}'.format(len(facilities)))
#     # print('Num customers {}'.format(len(customers)))

#     if time_limit is None:
#         time_limit = 5000 * 30 # 1 minute

#     solver = pywraplp.Solver('SolveIntegerProblem',
#                              pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
#     # x_i = 1 iff facility i is chosen
#     x = [] # 1xN
#     # y_ij = 1 iff custome j is assigned to facility i
#     y = [[] for x in range(len(facilities))] # NxM

#     for i in range(len(facilities)):
#         x.append(solver.BoolVar('x{}'.format(i)))
#         for j in range(len(customers)):
#             y[i].append(solver.BoolVar('y{},{}'.format(i,j)))

#     # print('x variable with dim {}'.format(len(x)))
#     # print('y variable with dim {}x{}'.format(len(y), len(y[0])))

#     # total demand to 1 facility <= its capacity
#     for i in range(len(facilities)):
#         constraint = solver.Constraint(0.0, facilities[i].capacity)
#         for j in range(len(customers)):
#             constraint.SetCoefficient(y[i][j], customers[j].demand)

#     # exactly one facility per customer
#     for j in range(len(customers)):
#         constraint = solver.Constraint(1.0, 1.0)
#         for i in range(len(facilities)):
#             constraint.SetCoefficient(y[i][j], 1.0)

#     # y_ij can be 1 only x_i is 1
#     for i in range(len(facilities)):
#         for j in range(len(customers)):
#             constraint = solver.Constraint(-solver.infinity(), 0.0)
#             constraint.SetCoefficient(y[i][j], 1.0)
#             constraint.SetCoefficient(x[i], -1.0)

#     # objective
#     objective = solver.Objective()
#     objective.SetMinimization()
#     for i in range(len(facilities)):
#         objective.SetCoefficient(x[i], facilities[i].setup_cost)
#         for j in range(len(customers)):
#             objective.SetCoefficient(y[i][j], length(customers[j].location, facilities[i].location))

#     # print('Number of variables =', solver.NumVariables())
#     # print('Number of constraints =', solver.NumConstraints())

#     solver.set_time_limit(time_limit)
#     # print('OR-Tools starts at {}'.format(datetime.now().time()))
#     result_status = solver.Solve()
#     # print(result_status)
#     # The problem has an optimal solution.
#     #assert result_status == pywraplp.Solver.OPTIMAL
#     #assert solver.VerifySolution(1e-7, True)

#     val = solver.Objective().Value()
#     y_val = [[] for x in range(len(facilities))] # NxM
#     assignment = []
#     for i in range(len(facilities)):
#         for j in range(len(customers)):
#             y_val[i].append(int(y[i][j].solution_value()))
#     y_val = numpy.array(y_val)
#     for j in range(len(customers)):
#         assignment.append(numpy.where(y_val[:,j]==1)[0][0])

#     return val, assignment

        

# import sys

# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         with open(file_location, 'r') as input_data_file:
#             input_data = input_data_file.read()
#         print(solve_it(input_data))
#     else:
#         print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from facility import facility
import numpy as np 
from random import randint
from ortools.linear_solver import pywraplp

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
  
    setup_cost = []
    capacity = []
    locationF = []
    demand = []
    locationC = []

    lines = input_data.split('\n')
    parts = lines[0].split()
    N = int(parts[0])
    M = int(parts[1])
    for i in range(1, N+1):
        parts = lines[i].split()
        setup_cost.append(float(parts[0]))
        capacity.append(int(parts[1]))
        locationF.append((float(parts[2]), float(parts[3])))
    
    for i in range(N+1, N+M+1):
        parts = lines[i].split()
        demand.append(int(parts[0]))
        locationC.append((float(parts[1]), float(parts[2])))
    
    distances = {}
    for from_counter, from_node in enumerate(locationF):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locationC):
            
            distances[from_counter][to_counter] = (float(
                math.hypot((from_node[0] - to_node[0]),
                (from_node[1]) - to_node[1])))
            #print(from_counter, to_counter, distances[from_counter][to_counter])

    if ((N <= 100) and (M <= 200)):
        fa = facility(N, M,distances, setup_cost,capacity, locationF, demand, locationC)
        best_output = fa.solve()
    else:  
        a = {}
        b = {}
        mask = {}
        f_open = {}
        
        for i in range(N):
            f_open[i] = 0

        for i in range(M):
            mask[i] = False

        cap = []
        for i in range(N):
            cap.append(capacity[i])
        for u in range(N):
            b[u] = []
        for v in range(M):
            u = -1
            minValue = 10000000
            for i in range(N):
                cost = distances[i][v] + setup_cost[i]
                if ((cost < minValue) and (demand[v] < cap[i])):
                    minValue = cost
                    u = i     
            if (u == -1):
                break
            else:
                a[v] = u 
                b[u].append(v)
                cap[u] = cap[u] - demand[v]
                f_open[u] = 1
                mask[v] = True
        obj = 0
        for i in range(M):
            obj += distances[a[i]][i]
        for i in range(N):
            obj += f_open[i] * setup_cost[i]
        best_objective = obj
        n_sub_facility = 5
        round_limit = 1000
        best_output = ''
        best_output += str(best_objective) + ' '+ '0' + '\n'

        for i in range(M):
            best_output += str(a[i])
            best_output += ' '
        
        run = 5000
        if (N == 200):
            run = 20000
        if (N >= 500):
            run = 50000
        n_facility = 5
        for step in range(run):
            #print(step)
            list_f = []
            count = 0
            while count < n_facility:
                while True:
                    tem = randint(0, N-1)
                    if tem not in list_f:
                        list_f.append(tem)
                        break
                count += 1
            list_cus = []
            for u in range(len(list_f)):
                for v in b[list_f[u]]:
                    list_cus.append(v)
            
            solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

            a_tem = {}
            X = {}

            objective_old = 0

            for u in list_f:
                for v in list_cus:
                    if a[v] == u:
                        objective_old += distances[u][v]
            
            
            for u in list_f:
                objective_old += f_open[u] * setup_cost[u]

            for u in list_f:
                X[u] = solver.IntVar(0,1,'X[%i]' % u)
            for u in list_f:
                a_tem[u] = {}
                for v in list_cus:
                    a_tem[u][v] = solver.IntVar(0, 1, 'a_tem[%i][%i]' %(u, v))

            for u in list_f:
                constraint = solver.RowConstraint(0, capacity[u], '')
                for v in list_cus:
                    constraint.SetCoefficient(a_tem[u][v], demand[v])
            
            for u in list_cus:
                constraint = solver.RowConstraint(1,1,'')
                for v in list_f:
                    constraint.SetCoefficient(a_tem[v][u], 1)
            
            for u in list_cus:
                for v in list_f:
                    solver.Add(a_tem[v][u] <= X[v])

            objective = solver.Objective()

            for u in list_f:
                for v in list_cus:             
                    objective.SetCoefficient(a_tem[u][v], distances[u][v])

            for u in list_f:
                objective.SetCoefficient(X[u], setup_cost[u])

            objective.SetMinimization()

            status = solver.Solve()
            if status == pywraplp.Solver.OPTIMAL:
                objective_new = solver.Objective().Value()
                if objective_old >= objective_new + 1:
                    best_objective -= objective_old - objective_new  
                    for u in list_f:
                        b[u] = []            
                    for v in list_cus:
                        for u in list_f:
                            if a_tem[u][v].solution_value() == 1:
                                a[v] = u
                                b[u].append(v)
                    
                    for u in list_f:
                        if X[u].solution_value() == 1:
                            f_open[u] = 1
                        else:
                            f_open[u] = 0
                
                best_output = ''

                best_output += str(best_objective) + ' '+ '0' + '\n'

                for i in range(M):
                    best_output += str(a[i])
                    best_output += ' '          
    
    return best_output




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
