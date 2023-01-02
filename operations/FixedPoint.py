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

    # def FixedPoint(self, G_X, relativeError, precision, x0, MaxIterations):
    #     def evaluation (x): return eval(G_X)
    #     cnt = 0
    #     error = relativeError
    #     oldX = x0
    #     Values = []
    #     steps = []
    #     while (MaxIterations != 0 and error >= relativeError):
    #         newX = self.round_sig(precision, evaluation(oldX)) 
    #         Values.append((oldX, newX))
    #         if newX != 0 : error = (abs(newX - oldX) / abs(newX)) * 100
    #         oldX = newX
    #         MaxIterations -= 1
    #         cnt += 1
    #         if newX != 0:
    #             steps.append("Iteration [" + str(cnt) + "]: x(i+1) = " + str(newX) + " (E): " + str(error) + " %")
    #         else :
    #             steps.append("Iteration [" + str(cnt) + "]: x(i+1) = " + str(newX) + " (E): skipped due to Division by 0") 

    #     return newX, steps, Values

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
        print(estimate_roots)
        return y, steps, estimate_roots
# [(3, 1.8000000000000003), (1.8000000000000003, 0.6480000000000002), (0.6480000000000002, 0.08398080000000006), (0.08398080000000006, 0.0014105549537280022), (0.0014105549537280022, 3.979330554973213e-07), (3.979330554973213e-07, 3.167014333148684e-14)]
if __name__ == '__main__':
    solver = FixedPoint()
    result, steps, values = solver.FixedPoint("0.2*x*x", 0.001, 5, 3, 30)
    print(result)
    for i in range(len(steps)):
        print(steps[i])


# pesoudo code for fixed point method

# while (MaxIterations != 0 and error >= relativeError){ // while loop for iterations
#     newX = Gx(oldX)
#     error = (abs(newX - oldX) / abs(newX)) * 100
#     oldX = newX
# }