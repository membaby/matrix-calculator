import copy
from math import *


class LUDecomposition:
    def __init__(self):
        self.operation_name = 'Gauss Elimination'
        self.n = 0
        self.sig = 5
        self.solution = []
        self.solution_steps = []
        self.order = []

    def get_solution(self, input_matrix, form, sig=5):
        self.sig = sig
        self.n = len(input_matrix)
        self.order = [k + 1 for k in range(self.n)]
        for l in range(self.n):
            self.solution.append(input_matrix[l].pop(self.n))
        if form == 'crout':
            input_matrix = self.transpose(input_matrix)
        flag = self.forward_elimination(input_matrix)
        if flag == 'Singular, no solution':
            return 'Singular, no solution', 'Singular, no solution'
        if form == 'crout':
            self.crout(input_matrix)
        elif form == 'cholesky':
            self.cholesky(input_matrix)
        elif form == 'doolittle':
            self.doolittle(input_matrix)
        return self.solution, self.solution_steps

    def round_sig(self, x):
        if x == 0:
            return 0
        return round(x, self.sig - int(floor(log10(abs(x)))) - 1)

    def forward_elimination(self, input_matrix):
        for k in range(self.n):
            i_max = k
            v_max = input_matrix[k][k]

            for l in range(k + 1, self.n):
                max_in_row = 0
                for j in range(l, self.n):
                    max_in_row = max(abs(input_matrix[l][j]), abs(max_in_row))

                if abs(input_matrix[l][k] / max_in_row > v_max):
                    i_max = l
                    v_max = input_matrix[l][k]

            if not v_max:
                return "Singular, no solution"

            if i_max != k:
                t = self.order[i_max]
                self.order[i_max] = self.order[k]
                self.order[k] = t
                for h in range(self.n):
                    temp = input_matrix[i_max][h]
                    input_matrix[i_max][h] = input_matrix[k][h]
                    input_matrix[k][h] = temp

            for l in range(k + 1, self.n):
                input_matrix[l][k] = self.round_sig((input_matrix[l][k]) / input_matrix[k][k])
                for j in range(k + 1, self.n):
                    input_matrix[l][j] = self.round_sig(input_matrix[l][j] - input_matrix[k][j] * input_matrix[l][k])

        return "Have a unique solution"

    def forward_substitution(self, input_matrix, ones):
        for k in range(self.n):
            for j in range(k):
                self.solution[k] -= self.round_sig(input_matrix[k][j] * self.solution[j])

            if not ones:
                self.solution[k] = self.round_sig(self.solution[k] / input_matrix[k][k])

    def back_substitution(self, input_matrix, ones):
        for k in range(self.n - 1, -1, -1):
            for j in range(k + 1, self.n):
                self.solution[k] -= self.round_sig(input_matrix[k][j] * self.solution[j])

            if not ones:
                self.solution[k] = self.round_sig(self.solution[k] / input_matrix[k][k])

    def transpose(self, matrix):
        for l in range(self.n):
            for j in range(l):
                temp = matrix[l][j]
                matrix[l][j] = matrix[j][l]
                matrix[j][l] = temp
        return matrix

    def reorder(self):
        solution = copy.deepcopy(self.solution)
        for o in range(self.n):
            self.solution[o] = solution[self.order[o] - 1]

    def crout(self, input_matrix):
        l = [[0 for _ in range(self.n)] for _ in range(self.n)]
        u = l
        for k in range(self.n):
            for j in range(k + 1):
                l[k][j] = input_matrix[k][j]
            u[k][k] = 1
            for j in range(k + 1, self.n):
                u[k][j] = input_matrix[k][j]
        text = f'Crout\'s LU:'
        self.solution_steps.append(text)
        var = []
        for o in range(self.n):
            var.append('X' + str(self.order[o]))
        text = f'{l}   {u}   {var}      {self.solution}'
        self.solution_steps.append(text)
        input_matrix = self.transpose(input_matrix)
        self.forward_substitution(input_matrix, False)
        text = f'{l}   {var}      {self.solution}'
        self.solution_steps.append(text)
        self.back_substitution(input_matrix, True)
        text = f'{var}      {self.solution}'
        self.solution_steps.append(text)
        solution = self.solution
        for o in range(self.n):
            self.solution[self.order[o] - 1] = self.round_sig(solution[o])

    def cholesky(self, input_matrix):
        self.reorder()
        d = [[0 for _ in range(self.n)] for _ in range(self.n)]
        l = copy.deepcopy(d)
        u = copy.deepcopy(l)
        for k in range(self.n):
            l[k][k] = 1
            for j in range(k):
                l[k][j] = input_matrix[k][j]
            u[k][k] = 1
            d[k][k] = input_matrix[k][k]
            for j in range(k + 1, self.n):
                input_matrix[k][j] /= input_matrix[k][k]
                u[k][j] = input_matrix[k][j]
        text = f'Cholesky\'s LU:'
        self.solution_steps.append(text)
        var = []
        for o in range(self.n):
            var.append('X' + str(self.order[o]))
        text = f'{l}   {d}   {u}   {var}      {self.solution}'
        self.solution_steps.append(text)
        self.forward_substitution(input_matrix, True)
        text = f'{l}   {d}   {var}      {self.solution}'
        self.solution_steps.append(text)
        for k in range(self.n):
            self.solution[k] /= input_matrix[k][k]
        text = f'{l}   {var}      {self.solution}'
        self.solution_steps.append(text)
        self.back_substitution(input_matrix, True)
        text = f'{var}      {self.solution}'
        self.solution_steps.append(text)
        for o in range(self.n):
            self.solution[o] = self.round_sig(self.solution[o])

    def doolittle(self, input_matrix):
        self.reorder()
        u = [[0 for _ in range(self.n)] for _ in range(self.n)]
        l = copy.deepcopy(u)
        for k in range(self.n):
            l[k][k] = 1
            for j in range(k):
                l[k][j] = input_matrix[k][j]
            for j in range(k, self.n):
                u[k][j] = input_matrix[k][j]
        text = f'Doolittle\'s LU:'
        self.solution_steps.append(text)
        var = []
        for o in range(self.n):
            var.append('X' + str(self.order[o]))
        text = f'{l}   {u}   {var}      {self.solution}'
        self.solution_steps.append(text)
        self.forward_substitution(input_matrix, True)
        text = f'{l}   {var}      {self.solution}'
        self.solution_steps.append(text)
        self.back_substitution(input_matrix, False)
        text = f'{var}      {self.solution}'
        self.solution_steps.append(text)
        for o in range(self.n):
            self.solution[o] = self.round_sig(self.solution[o])


if __name__ == '__main__':
    test_class = LUDecomposition()
    test_matrix = [
        [2, 1, 1, 1, 1, 4],
        [1, 2, 1, 1, 1, 5],
        [1, 1, 2, 1, 1, 6],
        [1, 1, 1, 2, 1, 7],
        [1, 1, 1, 1, 2, 8]
    ]
   # test = test_class.get_solution(copy.deepcopy(test_matrix), 'doolittle')
    #print(test)
    test = test_class.get_solution(copy.deepcopy(test_matrix), 'crout', 10)
    print(test)
   # test = test_class.get_solution(copy.deepcopy(test_matrix), 'cholesky')
    #print(test)
