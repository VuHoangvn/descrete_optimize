from ortools.linear_solver import pywraplp
import math

class facility:
    def __init__(self, N, M,distances, setup_cost,capacity, locationF, demand, locationC):
        self.N = N
        self.M = M
        self.setup_cost = setup_cost
        self.capacity = capacity
        self.locationF = locationF
        self.locationC = locationC
        self.demand = demand
        self.solver = pywraplp.Solver("facility", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.distances = distances

    def solve(self):
        infinity = self.solver.infinity()
        a = {}
        X = {}
        for u in range(self.N):
            X[u] = self.solver.IntVar(0,1,'X[%i]' % u)
        for u in range(self.N):
            a[u] = {}
            for v in range(self.M):
                a[u][v] = self.solver.IntVar(0, 1, 'a[%i][%i]' %(u, v))
        
        for u in range(self.N):
            constraint = self.solver.RowConstraint(0, self.capacity[u], '')
            for v in range(self.M):
                constraint.SetCoefficient(a[u][v], self.demand[v])
        
        for u in range(self.M):
            constraint = self.solver.RowConstraint(1,1,'')
            for v in range(self.N):
                constraint.SetCoefficient(a[v][u], 1)
        
        for u in range(self.M):
            for v in range(self.N):
                self.solver.Add(a[v][u] <= X[v])

        objective = self.solver.Objective()

        for u in range(self.N):
            #objective.SetCoefficient(X[u], self.setup_cost[u])
            for v in range(self.M):             
                objective.SetCoefficient(a[u][v], self.distances[u][v])

        for u in range(self.N):
            objective.SetCoefficient(X[u], self.setup_cost[u])

        objective.SetMinimization()
        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            output = ''
            output += str(self.solver.Objective().Value())
            output += ' 0\n'
            for u in range(self.M):
                for v in range(self.N):
                    if (a[v][u].solution_value() == 1):
                        output += str(v)
                        output += ' '
        return output

