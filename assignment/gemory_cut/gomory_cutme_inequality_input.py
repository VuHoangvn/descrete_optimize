from fractions import Fraction
from math import floor
# import numpy as np

# np.set_printoptions(suppress=True, formatter={'all':lambda x: str(Fraction(x).limit_denominator())})


class Gomory:
    def __init__(self, A, b, c):
        self.M = len(b)
        self.N = len(c)
        self.c = c
        self.b = b
        self.a = []
        for i in range(self.M + 1):
            temp = [Fraction(0) for _ in range(self.M + self.N + 1)]
            self.a.append(temp)
        
        for i in range(self.M):
            for j in range(self.N):
                self.a[i][j] = Fraction(A[i][j])

        for j in range(self.N, self.N + self.M):
            self.a[j-self.N][j] = Fraction(1)
        for j in range(self.N):
            self.a[self.M][j] = Fraction(c[j])
        
        
        
        # for j in range(self.N, self.M + self.N):
        #     self.a[self.M][j] = Fraction(1)

        for i in range(self.M):
            self.a[i][self.M + self.N] = Fraction(b[i])
        self.print_a()
        
    def pivot(self,p, q):
        for i in range(self.M + 1):
            for j in range(len(self.a[0])):
                if i != p and j != q:
                    self.a[i][j] -= self.a[p][j] * self.a[i][q] / self.a[p][q]
       
        for i in range(self.M + 1):
            if i != p:
                self.a[i][q] = Fraction(0)
        for j in range(len(self.a[0])):
            if j != q:
                self.a[p][j] /= self.a[p][q]
            
        self.a[p][q] = Fraction(1)

    def get_pivot(self):
        p = 0
        q = 0

        ## ?? self.a[self.M][q] max
        while q < len(self.a[0]) - 1:
            if self.a[self.M][q] > 0:
                break
            q += 1
        
        while p < self.M:
            if self.a[p][q] > 0:
                break
            p += 1

        return p, q

    def solve_simplex(self):
        print("hello")
        self.print_a()
        total_var = len(self.a[0])
        while True:
            p = 0
            q = 0

            ## ?? self.a[self.M][q] max
            while q < len(self.a[0]) - 1:
                if self.a[self.M][q] > 0:
                    break
                q += 1
            if q >= len(self.a[0]) - 1:
                break
            
            while p < self.M:
                if self.a[p][q] > 0:
                    break
                p += 1
            
            print('pivot: ', p, q)
            for i in range(p+1, self.M):
                if self.a[i][q] > 0:
                    if self.a[i][total_var - 1]/self.a[i][q] < self.a[p][total_var - 1]/self.a[p][q]:
                        p = i
            self.pivot(p, q)
            self.print_a()
        


    def print_a(self):
        for i in range(len(self.a)):
            print(self.a[i])
        print("===========================================")

    def get_cut(self, row):
        size = len(self.a)
        num_var = len(self.a[0])
        vir_var = num_var - self.M-1
        cut = []
        for i in range(num_var):
            cut.append(self.a[row][i])

        for i in range(vir_var):
            cut[i] = Fraction(0)
        
        for i in range(vir_var, num_var):
            cut[i] = floor(cut[i]) - cut[i]
        
        print("----------")
        print("cut")
        print(cut)
        print('----------')

        new_prob = self.a
        new_prob.insert(size-1, cut)
        for i in range(len(new_prob)):
            if i == len(new_prob) - 2:
                new_prob[i].insert(num_var - 1, Fraction(1))
            else:
                new_prob[i].insert(num_var - 1, Fraction(0))
        

        for i in range(len(new_prob)):
            print(new_prob[i])
        self.a = new_prob
        # self.print_a()
        # print("================================")

    def solve(self):
        print("--------------------------------")
        print('-----------start simplex -------')
        print("--------------------------------")

        self.solve_simplex()

        print("--------------------------------")
        print('-----------end simplex ---------')
        print("--------------------------------")

        print("********************************")

        print("--------------------------------")
        print('-----------start Gomory cut -------')
        print("--------------------------------")

        for idx, row in enumerate(self.a):
            if idx == len(self.a)-1:
                break
            count = 0

            for i in range(self.N):
                if row[i] == 0:
                    count += 1
            if count == self.N:
                self.a.remove(row)
        a = []
        for i in range(len(self.a)):
            a.append([])
            for j in range(self.N):
                a[i].append(self.a[i][j])
            a[i].append(self.a[i][-1])
        

        self.a = a
        for j in range(self.N):
            self.a[-1][j] = Fraction(c[j])
        self.a[-1][-1] = Fraction(0)
        self.print_a()

        print('------------cut----------------')
        
            
        has_cut = True
        while has_cut:
            has_cut = False
            for row in range(self.M):
                cnt = 0
                for i in range(len(self.a[row]) - 1):
                    if int(self.a[row][i].denominator == 1):
                        cnt += 1

                if int(self.a[row][-1].denominator) != 1:
                    
                    if cnt == len(self.a[row]) - 1:
                        print("This problem does not have integer solution!!!")
                        break
                if int(self.a[row][-1].denominator) == 1 and cnt == len(self.a[row]) - 1:
                    break
                else:
                    has_cut = True
                    self.get_cut(row)
                    
                    q = 0
                    min_val = 10000000
                    for i in range(self.M - 1, len(self.a[0])-1):
                        if self.a[-1][i] == 0 or self.a[-2][i] == 0:
                            continue

                        if self.a[-2][i]/self.a[-1][i] < min_val:
                            min_val = self.a[-2][i]
                            q = i

                    self.pivot(len(self.a) - 2, q)
                    print("===========================================")
                    self.print_a()
                    
# A = [
#     [3,2,1,0,0],
#     [5,1,1,1,0],
#     [2,5,1,0,1]
# ]
# b = [1,3,4]
# c = [1,1,1,1,1]

# A = [
#     [5, 15],
#     [4, 4],
#     [35, 20]
# ]

# b = [480, 160, 1190]

# c = [13, 23]

# A = [
#     [1, 0, 0, 1, 0, 6, 0],
#     [3, 1, -4, 0, 0, 2, 1],
#     [1, 2, 0, 0, 1, 2, 0]
# ]
# b = [9, 2, 6]
# c = [1, -6, 32, 1, 1, 10, 100]

# A = [
#     [-1, 3],
#     [7, 1]
# ]
# b = [6, 35]
# c = [7, 10]

# A = [
#     [-1, -1],
#     [2, -1]
# ]

# b = [1, 4]

# c = [1, -1]

# A = [
#     [1,1,1,1,1],
#     [1,1,2,2,2],
#     [1,1,0,0,0],
#     [0,0,1,1,1]
# ]

# b = [5,8,2,3]
# c = [2,1,1,0,0]

# A = [
#     [5, 15],
#     [4, 4],
#     [35, 20]
# ]

# b = [480, 160, 1190]
# c = [13, 23]

# A = [
#     [1, 0, 0],
#     [20, 1, 0],
#     [200, 20, 1]
# ]

# b = [1, 100, 100]
# c = [100, 10, 1]

# A = [
#     [3, 2],
#     [-3, 2]
# ]
# b = [6, 0]
# c = [0, 1]
#-------------------
# A = [
#     [2, 1, 0],
#     [2, -1, 1]
# ]
# b = [2, 5]
# c = [3, 2, 4]

# A = [
#     [5, 7, 4, 3]
# ]
# b = [14]
# c = [8, 11, 6, 4]

# A = [
#     [3, 2],
#     [-3, 2]
# ]
# b = [6, 0]
# c  = [0, 1]

# A = [
#     [1,2,2,1,0],
#     [1,2,3,0,-1]
# ]
# b = [Fraction(8,3), Fraction(7,3)]
# c = [3,4,1,0,0]

# A = [
#     [2,1],
#     [1,7]
# ]
# b = [4, 7]
# c = [1, 1]

# A = [
#     [3,2,1],
#     [2,3,3],
#     [-1,-1,1]
# ]
# b = [10, 15, -4]
# c = [2,3,4]

# A = [
#     [1,0,2,0],
#     [0,2,-8,0],
#     [0,-1,2,-1],
#     [1,1,1,1],
#     [1,0,0,0],
#     [0,1,0,0],
#     [0,0,1,0],
#     [0,0,0,1]
# ]
# b = [700,0,-1,10,10,10,10,10]
# c = [1,1,2,-2]

A = [
    [2,1,0],
    [2,-1,1]
]

b = [2, 5]
c = [3,2,4]

# A = [
#     [2,-2],
#     [-8,10]
# ]
# b = [-1, 13]
# c = [1,1]

## input dang bat dang thuc

simplex = Gomory(A, b, c)
simplex.solve()