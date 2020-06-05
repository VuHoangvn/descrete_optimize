import sys
import math
import numpy as np 
from fractions import Fraction

np.set_printoptions(suppress=True, formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

class Simplex:
    def __init__(self, filename, _print=False):
        # Input: Ax = b
        self.readdata(filename)
        self._print = _print
    
    def readdata(self, filename):
        # line 1: he so ham muc tieu
        # line 2: danh sach bien nguyen
        # line 2: rang buoc
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        self.c = [Fraction(i) for i in lines[0].split()]
        self.int_set = [int(i) for i in lines[1].split()]
        lines = np.array([[Fraction(i) for i in line.split()] for line in lines[2:]])
        self.b = lines[:, -1]
        self.A = lines[:, :-1]

    def pivot(self, p, q):
        # tinh toan phep bien doi don hinh
        a = self.a
        cur_base_var = self.cur_base_var
        M, N = a.shape
        a -= [[a[p][j] * a[i][q] / a[p][q] if i != p and j != q else 0 for j in range(N) ] for i in range(M)]
        a[p, :] = np.divide(a[p, :], [a[p][q] if j != q else 1 for j in range(N)])
        a[:, q] = np.array([Fraction(0) for _ in range(M)]).reshape(1, M) 
        a[p][q] = Fraction(1)
        cur_base_var[p] = q # xoa bien cu khoi co so va them bien moi vao co so
   
    def simplex_transform(self, method, phase=None):
        # lap lai bien doi don hinh den khi khong con phan tu tru
        cur_base_var = self.cur_base_var
        if self._print:
            print('Step 0: ',' base = ' , ['X' + str(i+1) for i in cur_base_var], '\n' + self.get_pretty_print_tableau())
            print('======================================================================================================')
        it = 0
        while(True):
            if method == 'simplex': p, q = self.get_pivot(phase)
            elif method == 'dual_simplex': 
                p, q = self.get_pivot_dual_simplex()
            if p == -1 or q == -1: 
                if method == 'dual_simplex':
                    if p >= 0 and q == -1:
                        return False
                    elif p == -1:
                        return True
                elif method == 'simplex':
                    if q >= 0 and p == -1:
                        return False
                    elif q == -1:
                        return True
                break
            self.pivot(p, q)
            it += 1
            if self._print:
                print('Step', it, ': ', 'pivot = ', p, q, ', base = ', ['X' + str(i+1) for i in cur_base_var] , '\n' + self.get_pretty_print_tableau())
                print('======================================================================================================')
    
    def gomory_cut(self, row):
        if self._print:
            print('gomory cut on X[' + str(self.cur_base_var[row]+1) + ']')
            print('======================================================================================================')
        M, N = self.a.shape
        cur_row = self.a[row, :]
        gomory_constraint = [Fraction(math.floor(i) - i) if i not in self.cur_base_var else Fraction(0) for i in cur_row]
        new_varible = np.array([Fraction(0) for i in range(M+1)]).reshape(1, M+1)
        new_varible[:, -2] = Fraction(1)
        self.a = np.insert(self.a, M-1, [gomory_constraint], axis=0)
        self.a = np.insert(self.a, N-1, new_varible, axis=1)
        self.cur_base_var.append(self.a.shape[1]-2)
    
    def branch_bound(self, row):


    def solve_phase_1(self):
        # tao bang don hinh
        M, N = self.A.shape
        self.a = np.array([[Fraction(x) for x in y] for y in self.A])
        self.a = np.append(self.a, np.reshape([Fraction(i) for i in self.b], (self.a.shape[0], 1)), axis=1)
        # tao he so ham muc tieu cua bai toan phu
        c1 = np.sum(self.a[:M, :-1], axis=0) # cong c' voi cac rang buoc de tao ma tran rang buoc co cac bien co so bang 0
        c1 = np.append(c1, np.array([Fraction(0) for i in range(M)])) # them vao bang he so ham muc tieu bai toan phu
        c1 = np.append(c1, Fraction(np.sum(self.a[:, -1])))
        # tao ma tran don vi
        I = [[Fraction(j) for j in i] for i in np.identity(M)]
        self.a = np.append(np.append(self.a[:, :-1], I, axis=1), self.a[:, -1:], axis=1) # them bien phu vao ma tran rang buoc 
        # them he so ham muc tieu bai toan chinh vao cuoi bang
        self.a = np.append(self.a, [np.append(self.c, np.array([Fraction(0) for i in range(M+1)]))], axis=0) 
        self.a = np.append(self.a, [c1], axis=0)
        self.cur_base_var = [i + N for i in range(M)] # co so ban dau
        self.artificial_var = self.cur_base_var.copy()
        if self._print:
            print('Begin phase 1', '\n')
        self.simplex_transform('simplex', phase=1)
        M, N = self.A.shape
        if self.a[-1, -1] != 0:
            if self._print:
                print('Khong co phuong an toi uu, thuat toan ket thuc tai pha 1')
            return False
        else:
            i = 0
            while i < len(self.cur_base_var):
                removed = False
                # Neu trong co so con ton tai bien gia
                if self.cur_base_var[i] in self.artificial_var:
                    if self.a[i, -1] != 0:
                        # mot trong cac bien gia khac 0
                        if self._print:
                            print('Khong co phuong an toi uu, thuat toan ket thuc tai pha 1')
                        return False
                    for index1, j in enumerate(self.a[i, 0:N]):
                        if index1 not in self.cur_base_var and j != 0:
                            # loai bien gia khoi co so va thay vao bien that
                            self.pivot(i, index1)
                            removed = True
                            break
                    # rang buoc chi con bien gia, xoa rang buoc
                    if not removed:
                        self.a = np.delete(self.a, i, axis=0)
                        del self.cur_base_var[i]
                        i -= 1
                i += 1
            # xoa bien phu khoi ma tran rang buoc
            M, N = self.A.shape
            # xoa cac cot bien gia
            self.a = np.delete(self.a, range(N, M + N), axis=1)  
            # xoa he so ham muc tieu cua bai toan phu
            self.a = np.delete(self.a, self.a.shape[0] - 1, axis=0)
        return True
        
    def solve_phase_2(self):
        if self._print:
            print('Begin phase 2: ', '\n' )
        if self.simplex_transform('simplex'):
            return True
        else:
            if self._print:
                print('Khong tim duoc nghiem ,thuat toan ket thuc tai pha 2')
            return False
    
    def get_pivot(self, phase=None):
        a = self.a
        cur_base_var = self.cur_base_var
        #lay ra vi tri phan tu tru
        p = -1
        q = -1
        min_value = 0
        row = -1
        if phase == 1:
            row = -2
        for index, value in enumerate(a[-1, :-1]):
            # lay ra he so ham muc tieu lon hon 0 va lon nhat lam cot
            if value > 0 and value > min_value and index not in cur_base_var:
                min_value = value
                q = index
        if q == -1:
            return -1, -1
        min_value = sys.maxsize
        for index, value in enumerate(a[:row, q]):
            # lay ra hang co ti le duong va nho nhat, phan tu chon lam pivot phai > 0
            if value > 0:
                ratio = a[:row, -1][index] / value
                if ratio >= 0 and ratio < min_value:
                    min_value = ratio
                    p = index
        return p, q

    def get_pivot_dual_simplex(self):
        a = self.a
        cur_base_var = self.cur_base_var
        #lay ra vi tri phan tu tru
        p = -1
        q = -1
        min_value = 0
        for index, value in enumerate(a[:-1, -1]):
            if value < 0 and value < min_value:
                min_value = value
                p = index
        if p == -1:
            return -1, -1
        min_value = sys.maxsize
        for index, value in enumerate(a[p, :-1]):
            if value < 0 and index not in cur_base_var :
                ratio = a[-1, :][index] / value
                if ratio < min_value:
                    min_value = ratio
                    q = index
        return p, q

    

    def gomory_solver(self):
        if not self.solve_phase_1():
            return False
        if not self.solve_phase_2():
            return False
        i = 0
        while(i < len(self.cur_base_var)):
        # for index, i in enumerate(self.cur_base_var):
            if self.cur_base_var[i] in self.int_set and self.a[:-1, -1][i].denominator != 1:
                self.gomory_cut(i)
                if self._print:
                    print('Begin dual simplex:\n')
                if not self.simplex_transform('dual_simplex'):
                    return False
                i = -1
            i += 1
        return True
    
    def branch_bound_solver(self):
        if not self.solve_phase_1():
            return False
        if not self.solve_phase_2():
            return False
        i = 0
        while(i < len(self.cur_base_var)):
        # for index, i in enumerate(self.cur_base_var):
            if self.cur_base_var[i] in self.int_set and self.a[:-1, -1][i].denominator != 1:
                self.gomory_cut(i)
                if self._print:
                    print('Begin dual simplex:\n')
                if not self.simplex_transform('dual_simplex'):
                    return False
                i = -1
            i += 1
        return True

    def printSolution(self):
        if self.gomory_solver():
            varible = ['X' + str(i+1) + ' = ' + str(self.a[:-1, -1][self.cur_base_var.index(i)]) if i in self.cur_base_var else 'X' + str(i+1) + ' = 0'  for i in range(self.A.shape[1])]
            print('Solution: ', varible, ' optimal value = ', -self.a[-1, -1])
   
    def get_pretty_print_tableau(self):
        a1 = self.a.copy()
        b1 = ['X'+ str(x+1) + '  |' for x in self.cur_base_var]
        b1 = np.append(b1, [' ' for i in range(a1.shape[0] - len(self.cur_base_var))])
        b1 = np.reshape(b1, (a1.shape[0], 1))
        a1 = np.append(b1, a1, axis=1)
        s = [[str(e) if type (e) is str or ((type(e) is Fraction or type(e) is int) and e < 0) else ' ' + str(e) for e in row] for row in a1]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)


s = Simplex('in_2.txt', True)
s.printSolution()
