from ortools.sat.python import cp_model

def NQueen(num_queens):
    model = cp_model.CpModel()
    row = [model.NewIntVar(1, num_queens, 'q'+str(i)) for i in range(1, num_queens+1)]
    col = [model.NewIntVar(1, num_queens, 'q'+str(i)) for i in range(1, num_queens+1)]
    
    diag1 = []
    diag2 = []
    c_diag1 = []
    c_diag2 = []

    # for i in range(num_queens-1):
    #     for j in range(i+1, num_queens):
    #         model.Add(row[i] != row[j])
    #         model.Add(row[i] != (row[j] + (j + i)))
    #         model.Add(row[i] != (row[j] - (j - i)))
    
    # for i in range(num_queens-1):
    #     for j in range(i+1, num_queens):
    #         model.Add(col[i] != col[j])
    #         model.Add(col[i] != (col[j] + (j + i)))
    #         model.Add(col[i] != (col[j] - (j - i)))
    i = 0
    for r in row:
        for c in col:
            # model.AddElement(c,col,r)
            t = model.NewBoolVar('t_%i' % i)
            
            model.AddElement(c,row,r).OnlyEnforceIf(t)
            model.AddElement(r,col,c).OnlyEnforceIf(t)

            i += 1


    for i in range(num_queens-1):
        diag1.append(model.NewIntVar(0, 2*num_queens-2, 'diag1'+str(i)))
        model.Add(diag1[i] == (row[i] + i))
        diag2.append(model.NewIntVar(-num_queens+1, num_queens-1, 'diag2'+str(i)))
        model.Add(diag2[i] == (row[i] - i))
    for i in range(num_queens-1):
        c_diag1.append(model.NewIntVar(0, 2*num_queens-2, 'c_diag1'+str(i)))
        model.Add(c_diag1[i] == (col[i] + i))
        c_diag2.append(model.NewIntVar(-num_queens+1, num_queens-1, 'c_diag2'+str(i)))
        model.Add(c_diag2[i] == (col[i] - i))

    model.AddAllDifferent(row)
    model.AddAllDifferent(diag1)
    model.AddAllDifferent(diag2)
    model.AddAllDifferent(col)
    model.AddAllDifferent(c_diag1)
    model.AddAllDifferent(c_diag2)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        for i in range(num_queens):
            print('q = %i' % solver.Value(row[i]))

NQueen(50)