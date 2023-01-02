import math
from math import *

class FixedPoint:
    def __init__(self):
        self.operation_name = 'Fixed Point'
        self.solution_steps = []

    def round_sig(self, sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def FixedPoint(self, equation, relativeError, precision, x, MaxIterations):
        steps = []
        f = lambda x: eval(equation)
        y = f(x)
        
        cnt = 0
        estimate_roots = [(x, y)]
        while (MaxIterations != 0 and abs(y-x) >= relativeError):
            x = f(x)
            cnt += 1
            MaxIterations -= 1
            y = f(x)
            estimate_roots.append((x, y))
            if y != 0:
                error = (abs(y - x) / abs(y)) * 100
                steps.append("Iteration [" + str(cnt) + "]: x(i+1) = " + str(y) + " (E): " + str(error) + " %")
            else:
                steps.append("Iteration [" + str(cnt) + "]: x(i+1) = " + str(y) + " (E): skipped due to Division by 0") 
        return y, steps, estimate_roots

if __name__ == '__main__':
    solver = FixedPoint()
    result, steps, values = solver.FixedPoint("exp(x)", 0.001, 5, 3, 30)
    print(result)
    for i in range(len(steps)):
        print(steps[i])