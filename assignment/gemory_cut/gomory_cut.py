from fractions import Fraction

class Gomory:
    def __init__(self, A, b, c):
        self.M = len(b)
        self.N = len(c)
        self.A = A
        self.b = b
        self.c = c
        self.a = [[Fraction(0) for i in range(self.M + self.N + 1)] for j in range(self.M + 2)]
        self.basis = [(self.N + i) for i in range(self.M)]
s = Simplex('input/in_1.txt', True)
s.printSolution()
        # a[i][j] = A[i][j]
        for i in range(self.M):
            for j in range(self.N):
                self.a[i][j] = Fraction(self.A[i][j])

        # artificial variables
        for i in range(self.M):
            self.a[i][self.N + i] = Fraction(1)
            self.a[self.M + 1][self.N + i] = Fraction(1)

        # b
        for i in range(self.M):
            self.a[i][self.M + self.N] = Fraction(b[i])

        # add objective function as an equation in row M + 1
        for i in range(self.N):
            self.a[self.M + 1][i] = Fraction(-c[i])

        # add phase 1 objective in row M
        for j in range(self.M + self.N + 1):
            for i in range(self.M):
                self.a[self.M][j] += self.a[i][j]

    # select pivot column by finding the most negative indicator (a[M][0, N + M])
    def select_pivot_col(self):
        col = -1
        min_negative = 0
        for i in range(0, self.N + self.M):
            if self.a[self.M][i] < 0 and self.a[self.M][i] < min_negative:
                min_negative = self.a[self.M][i]
                col = i
        return col

    # select pivot row after selected a pivot column
    # min positive a[i][M+N] / a[i][col] when a[i][col] > 0
    def select_pivot_row(self, col):
        row = -1
        min_positive = Fraction(100000)
        for i in range(self.M):
            if self.a[i][col] > 0:
                temp = Fraction(self.a[i][self.M + self.N], self.a[i][col])
                if temp < min_positive:
                    min_positive = temp
                    row = i
        return row

    def pivot(self, row, col):
        # pivot row
        pivot_val = self.a[row][col]
        for i in range(self.M + self.N + 1):
            self.a[row][i] = self.a[row][i] / pivot_val

        # other row
        for i in range(self.M + 2):
            if i != row:
                coef = Fraction(-self.a[i][col], pivot_val)
                for j in range(self.M + self.N + 1):
                    self.a[i][j] = self.a[i][j] + coef * self.a[row][j]

        self.basis[row] = col

    def print_result(self):
        print('optimal value = ', self.a[self.M][self.M + self.N])
        print('result: ')
        for i in range(self.M):
            print('x[', self.basis[i], '] =', self.a[i][self.M + self.N])
        print('****************************')

    def print_a(self):
        for i in range(len(self.a)):
            if i < self.M:
                print(self.basis[i], '| ', end='')
            else:
                print('    ', end='')
            for j in range(len(self.a[i])):
                print(self.a[i][j], end='   ')
            print()
        print("===========================================")

    def phase_one(self):
        print('phase 1:')
        while True:
            self.print_a()
            col = self.select_pivot_col()
            if col < 0:
                break
            row = self.select_pivot_row(col)
            if row < 0:
                break
            print("pivot:", row, col)
            self.pivot(row, col)

    def init_phase_two(self):
        # check feasible solution or not
        temp = self.a[self.M]
        self.a[self.M] = self.a[self.M + 1]
        self.a[self.M + 1] = temp

    def phase_two(self):
        print('phase 2:')
        while True:
            self.print_a()
            col = self.select_pivot_col()
            if col < 0:
                break
            row = self.select_pivot_row(col)
            if row < 0:
                break
            print("pivot:", row, col)
            self.pivot(row, col)

            for i in range(self.M + 2):
                for j in range(self.N, self.N + self.M):
                    self.a[i][j] = Fraction(0)

    def two_phase_simplex(self):
        self.phase_one()
        self.init_phase_two()
        self.phase_two()
        self.print_result()


    # def gomory_cut
    # def dual_simplex

if __name__ == '__main__':
    # A = [
    #     [2, 1],
    #     [2, 3]
    # ]
    # b = [8, 12]
    # c = [3, 1]

    A = [
        [2, 1, 0],
        [2, -1, 1]
    ]
    b = [2, 5]
    c = [3, 2, 4]

    gomory = Gomory(A, b, c)
    gomory.two_phase_simplex()
