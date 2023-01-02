from math import *


class FixedPoint:
    def __init__(self):
        self.operation_name = 'Fixed Point'
        self.solution_steps = []

    @staticmethod
    def round_sig(sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def fixed_point(self, equation, relative_error, precision, x, max_iterations):
        f = lambda x: eval(equation)
        y = f(x)

        cnt = 0
        estimate_roots = [(x, y)]
        while max_iterations != 0 and abs(y - x) >= relative_error:
            x = self.round_sig(precision, f(x))
            cnt += 1
            max_iterations -= 1
            y = self.round_sig(precision, f(x))
            estimate_roots.append((x, y))
            if y != 0:
                error = (abs(y - x) / abs(y)) * 100
                self.solution_steps.append(
                    "Iteration [" + str(cnt) + "]: x(i+1) = " + str(y) + " (E): " + str(error) + " %")
            else:
                self.solution_steps.append(
                    "Iteration [" + str(cnt) + "]: x(i+1) = " + str(y) + " (E): skipped due to Division by 0")
        return y, self.solution_steps, estimate_roots


if __name__ == '__main__':
    solver = FixedPoint()
    result, steps, values = solver.fixed_point("exp(x)", 0.001, 5, 3, 30)
    print(result)
    for i in range(len(steps)):
        print(steps[i])
