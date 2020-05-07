
class Simplex:
    def __init__(self, A, b, c):
        self.M = len(b)
        self.N = len(c)
        self.a = []
        for i in range(self.M + 1):
            temp = [0 for _ in range(self.M + self.N + 1)]
            self.a.append(temp)
        
        for i in range(self.M):
            for j in range(self.N):
                self.a[i][j] = A[i][j]

        for j in range(self.N, self.N + self.M):
            self.a[j-self.N][j] = 1.0
        for j in range(self.N):
            self.a[self.M][j] = c[j]
        for i in range(self.M):
            self.a[i][self.M + self.N] = b[i]
        
    def pivot(self,p, q):
        for i in range(self.M + 1):
            for j in range(self.M + self.N + 1):
                if i != p and j != q:
                    self.a[i][j] -= self.a[p][j] * self.a[i][q] / self.a[p][q]
       
        for i in range(self.M + 1):
            if i != p:
                self.a[i][q] = 0.0
        for j in range(self.M + self.N):
            if j != q:
                self.a[p][j] /= self.a[p][q]
            
        self.a[p][q] = 1.0

    def solve(self):
        while True:
            p = 0
            q = 0
            while q < self.M + self.N:
                if self.a[self.M][q] > 0:
                    break
                q += 1
            if q >= self.M + self.N:
                break
            
            while p < self.M:
                if self.a[p][q] > 0:
                    break
                p += 1
            

            for i in range(p+1, self.M):
                if self.a[i][q] > 0:
                    if self.a[i][self.M + self.N]/self.a[i][q] < self.a[p][self.M + self.N]/self.a[p][q]:
                        p = i
            
            self.pivot(p, q)
        

A = [
    [3,2,1,0,0],
    [5,1,1,1,0],
    [2,5,1,0,1]
]
b = [1,3,4]
c = [1,1,1,1,1]

# A = [
#     [1, 0, 0, 1, 0, 6, 0],
#     [3, 1, -4, 0, 0, 2, 1],
#     [1, 2, 0, 0, 1, 2, 0]
# ]
# b = [9, 2, 6]
# c = [1, -6, 32, 1, 1, 10, 100]

simplex = Simplex(A, b, c)
simplex.solve()