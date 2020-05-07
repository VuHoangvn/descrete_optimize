from fractions import Fraction
from math import floor


class Gomory:
    def __init__(self, A, b, c):
        self.M = len(b)
        self.N = len(c)
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
        for i in range(self.M):
            self.a[i][self.M + self.N] = Fraction(b[i])
        
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
            

            for i in range(p+1, self.M):
                if self.a[i][q] > 0:
                    if self.a[i][total_var - 1]/self.a[i][q] < self.a[p][total_var - 1]/self.a[p][q]:
                        p = i
            
            self.pivot(p, q)

    def get_cut(self, row):
        size = len(self.a)
        num_var = len(self.a[0])
        vir_var = num_var - self.M - 1
        cut = []
        for i in range(num_var):
            cut.append(self.a[row][i])

        for i in range(vir_var):
            cut[i] = Fraction(0)
        
        for i in range(vir_var, num_var):
            cut[i] = floor(cut[i]) - cut[i]
        
        print("----------")
        print(cut)
        print('----------')

        new_prob = self.a
        new_prob.insert(size-1, cut)
        for i in range(len(new_prob)):
            if i == len(new_prob) - 2:
                new_prob[i].insert(num_var - 1, Fraction(1))
            else:
                new_prob[i].insert(num_var - 1, Fraction(0))
        

        print("cut")
        for i in range(len(new_prob)):
            print(new_prob[i])
        self.a = new_prob
        print('==========================================')

    def solve(self):
        self.solve_simplex()
        for row in range(self.M):
            
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

            for i in range(len(self.a)):
                print(self.a[i])
            print('==========================================')
        

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

A = [
    [-1, 3],
    [7, 1]
]
b = [6, 35]
c = [7, 10]

simplex = Gomory(A, b, c)
simplex.solve()