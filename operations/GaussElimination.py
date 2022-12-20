class GaussElimination:
    def __init__(self):
        self.operation_name = 'Gauss Elimination'
        self.n = 0
        self.solutions = []
        self.solution_steps = []

    def get_solution(self, input_matrix):
        self.n = len(input_matrix)
        self.solutions = [0 for _ in range(self.n)]
        flag = self.forward_elimination(input_matrix)
        if flag == "Have a unique solution":
            self.back_substitution(input_matrix)
            return [round(x, 8) for x in self.solutions], self.solution_steps
        elif flag == "Singular and have no solution":
            return "Singular and have no solution", "Singular and have no solution"
        else:
            return self.infinite_number(input_matrix, flag), self.solution_steps

    def forward_elimination(self, input_matrix):
        for k in range(self.n):
            self.solution_steps.append([row[:] for row in input_matrix])
            i_max = k
            v_max = input_matrix[i_max][k]

            for i in range(k + 1, self.n):
                max_in_row = 0
                for j in range(i, self.n + 1):
                    max_in_row = max(abs(input_matrix[i][j]), abs(max_in_row))

                if abs(input_matrix[i][k] / max_in_row > v_max):
                    v_max = input_matrix[i][k]
                    i_max = i

            if not v_max:
                if input_matrix[k][self.n] == 0:
                    return k
                else:
                    return "Singular and have no solution"

            if i_max != k:
                for h in range(self.n + 1):
                    temp = input_matrix[i_max][h]
                    input_matrix[i_max][h] = input_matrix[k][h]
                    input_matrix[k][h] = temp

                self.solution_steps.append([row[:] for row in input_matrix])

            for i in range(k + 1, self.n):
                factor = (input_matrix[i][k]) / input_matrix[k][k]
                self.solution_steps.append(factor)
                input_matrix[i][k] = 0
                for j in range(k + 1, self.n + 1):
                    input_matrix[i][j] = round(input_matrix[i][j] - input_matrix[k][j] * factor, 8)

        return "Have a unique solution"

    def back_substitution(self, input_matrix):
        for i in range(self.n - 1, -1, -1):
            self.solutions[i] = input_matrix[i][self.n]

            for j in range(i + 1, self.n):
                self.solutions[i] -= input_matrix[i][j] * self.solutions[j]

            self.solutions[i] = (self.solutions[i] / input_matrix[i][i])

    def infinite_number(self, input_matrix, k):
        self.solutions = []
        for i in range(self.n - k, -1, -1):
            sol = ''
            for j in range(i + 1, self.n):
                sol += str(input_matrix[i][j]) + '*X' + str(j) + ' + '
            sol = sol[:len(sol) - 3]
            sol += ' = ' + str(input_matrix[i][self.n])
            self.solutions.append(sol)
        return self.solutions


if __name__ == '__main__':
    test_class = GaussElimination()
    test_matrix = [
        [144, 12, 1, 279.2],
        [64, 8, 1, 177.2],
        [25, 5, 1, 106.8]
    ]
    solutions, solution_steps = test_class.get_solution(test_matrix)
    print(solutions)
    print('xxxx')
    print(solution_steps)
