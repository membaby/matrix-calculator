import copy
from math import log10, floor


class JacobiIteration:
    def __init__(self):
        self.operation_name = 'Jacobi Iteration Method'
        self.solution = []
        self.solution_steps = []

    @staticmethod
    def round_sig(x, sig=5):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def get_solution(self, coefficient_matrix, b, initial_guess, relative_error):
        temp = copy.deepcopy(initial_guess)
        x = copy.deepcopy(initial_guess)
        max_no_iterations = 0
        e = relative_error
        while max_no_iterations != 100 and e >= relative_error:
            e = 0
            for i in range(len(b)):
                numerator = b[i]
                for j in range(len(b)):
                    if i != j:
                        numerator -= x[j] * coefficient_matrix[i][j]
                temp[i] = self.round_sig(numerator / coefficient_matrix[i][i])

            # take e after each iteration
            for i in range(len(b)):
                new_error = (abs(temp[i] - x[i]) / temp[i]) * 100
                e = max(e, new_error)

            # after end of each iteration take a copy to x
            x = copy.deepcopy(temp)
            max_no_iterations += 1
            text = f'Iteration [{max_no_iterations}]: X = {x} (E: {e})'
            self.solution_steps.append(text)
        self.solution = x
        return self.solution, self.solution_steps


if __name__ == '__main__':
    test_class = JacobiIteration()
    a = [
        [12, 3, -5],
        [1, 5, 3],
        [3, 7, 13]
    ]
    bs = [1, 28, 76]
    initialGuess = [1, 0, 1]
    test = test_class.get_solution(a, bs, initialGuess, 0.8)
    print(test)
