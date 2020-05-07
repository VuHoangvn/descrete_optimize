from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model

def MagicSeries(num):
    model = cp_model.CpModel()

    series = [model.NewIntVar(0, num-1, 's'+str(i)) for i in range(num)]

    for i in range(num):
        eq = []
        for j in range(num):
            t = model.NewBoolVar('t_%i_%i' % (i, j))
            model.Add(series[j] == i).OnlyEnforceIf(t)
            model.Add(series[j] != i).OnlyEnforceIf(t.Not())
            eq.append(t)
        model.Add(series[i] == sum(eq))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        for i in range(num):
            print(solver.Value(series[i]))



MagicSeries(5)