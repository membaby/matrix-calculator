import math
import numpy as np


class GaussJordan:

    def __init__(self):
        self.operation_name = 'Gauss Jordan Elimination'
        self.solution = []
        self.solution_steps = []

    def round_sig(self, x, digits=6):
        if x == 0 or not math.isfinite(x):
            return x
        digits -= math.ceil(math.log10(abs(x)))
        return round(x, digits)

    def partialPivoting(self, input_matrix, b, rows, curr):
        # find the pivot row
        pivot = curr
        for i in range(curr + 1, rows):
            # just comparing values
            if abs(input_matrix[i][curr]) > abs(input_matrix[pivot][curr]):
                pivot = i

        # swap the rows
        if pivot != curr:
            tmp = input_matrix[curr]
            input_matrix[curr] = input_matrix[pivot]
            input_matrix[pivot] = tmp
            aug_tmp = b[curr]
            b[curr] = b[pivot]
            b[pivot] = aug_tmp

    def checkRank(self, input_matrix):
        rank = np.linalg.matrix_rank(input_matrix)
        return rank

    def getSolution(self, input_matrix, precision=6):

        rankAugA = self.checkRank(input_matrix)  # rank of augmented matrix
        rows = len(input_matrix)
        # last column is the augmented matrix
        columns = len(input_matrix[0]) - 1
        for i in range(rows):
            for j in range(columns + 1):
                input_matrix[i][j] = self.round_sig(
                    input_matrix[i][j], precision)

        b = [input_matrix[i][columns]
             for i in range(columns)]  # set the last column as b

        # extract the b part from input matrix
        for i in range(rows):
            input_matrix[i] = input_matrix[i][0:columns]

        rankA = self.checkRank(input_matrix)  # rank of matrix

        # check if the system has one solution, infinite solutions or no solution
        if rankA < rankAugA:
            return ['No solution'], ['No solutions found for this set of equations!']
        elif rankA == rankAugA:
            if rankA < columns:
                return ['Infinite solutions'], ['An infinite number of solutions was found for this set of equations!']

        # forward elimination
        for i in range(rows):
            self.partialPivoting(input_matrix, b, rows, i)
            self.solution_steps.append([row[:] for row in input_matrix])
            for j in range(i + 1, columns):
                multiplier = input_matrix[j][i] / input_matrix[i][i]
                for k in range(i, columns):
                    input_matrix[j][k] = self.round_sig(
                        input_matrix[j][k] - multiplier * input_matrix[i][k], precision)
                b[j] = self.round_sig(b[j] - multiplier * b[i], precision)

        # backward elimination
        for i in range(rows - 1, -1, -1):
            self.solution_steps.append([row[:] for row in input_matrix])
            for j in range(i - 1, -1, -1):
                multiplier = input_matrix[j][i] / input_matrix[i][i]
                for k in range(i, columns):
                    input_matrix[j][k] = self.round_sig(
                        input_matrix[j][k] - multiplier * input_matrix[i][k], precision)
                b[j] = self.round_sig(b[j] - multiplier * b[i], precision)

        # get the solution
        for i in range(rows - 1, -1, -1):
            b[i] = self.round_sig(b[i] / input_matrix[i][i], precision)
            input_matrix[i][i] = input_matrix[i][i] / input_matrix[i][i]
            x = self.round_sig(b[i] / input_matrix[i][i], precision)
            self.solution.append(x)

        solution = [self.round_sig(x, precision) for x in self.solution]
        for idx in range(len(solution)):
            solution[idx] = f'X{idx} = ' + str(solution[idx])

        return solution, self.solution_steps


if __name__ == '__main__':
    test_class = GaussJordan()
    test_matrix = [
        [4, 7, 1, 2],
        [0, 3, 5, 0],
        [1, 0, -1, 1],
    ]

    solution_steps, solutions = test_class.getSolution(
        test_matrix, precision=6)
    print(solution_steps)
    print(solutions)
