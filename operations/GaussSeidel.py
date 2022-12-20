from math import log10, floor


class GaussSeidel:
    def __init__(self):
        self.operation_name = 'Gauss Seidel Elimination'
        self.solution = []
        self.solution_steps = []

    @staticmethod
    def round_sig(x, sig=5):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def get_solution(self, coefficient_matrix, b, initial_guess, relative_error):
        x = initial_guess
        max_no_iterations = 0
        e = relative_error
        while max_no_iterations != 100 and e >= relative_error:
            e = 0
            for i in range(len(b)):
                numerator = b[i]
                for j in range(len(b)):
                    if i != j:
                        numerator -= x[j] * coefficient_matrix[i][j]

                old_x = x[i]
                x[i] = self.round_sig(numerator / coefficient_matrix[i][i])
                new_x = x[i]
                new_error = (abs(new_x - old_x) / new_x) * 100
                e = max(e, new_error)

            max_no_iterations += 1
            text = f'Iteration [{max_no_iterations}]: X = {x} (E: {e})'
            self.solution_steps.append(text)
        self.solution = x
        return self.solution, self.solution_steps


if __name__ == '__main__':
    test_class = GaussSeidel()
    a = [
        [12, 3, -5],
        [1, 5, 3],
        [3, 7, 13]
    ]
    bs = [1, 28, 76]
    initialGuess = [1, 0, 1]
    test = test_class.get_solution(a, bs, initialGuess, 0.8)
    print(test)
