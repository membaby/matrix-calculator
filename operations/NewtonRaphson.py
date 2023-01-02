from sympy import *
from math import *
import matplotlib.pyplot as plt
import numpy as np

class NewtonRaphson:
    def __init__(self):
        self.operation_name = 'Newton Raphson'
        self.solution = ''
        self.steps = []
        self.estimate_roots = []
    
    def round_sig(self, sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def getSolution(self, equation, x0, tolerance, max_iterations, precision):
        x0 = self.round_sig(precision, x0)
        self.equation = equation
        x = Symbol('x')
        step = 1
        flag = 1
        condition = True
        def func(x): return self.round_sig(precision, eval(equation))
        derivative = Derivative(equation, 'x').doit()
        self.steps.append(f'Iteration #0: Xi+1 = {x0}, f(Xi+1) = {func(x0)}')
        self.estimate_roots.append(x0)
        while condition:
            if derivative.subs(x, x0) == 0.0:
                return 'Divide by zero error!', self.steps

            x1 = self.round_sig(precision, x0 - func(x0)/derivative.subs(x, x0))
            self.steps.append(f'Iteration #{step}: Xi+1 = {x1}, f(Xi+1) = {func(x1)}')
            self.estimate_roots.append(x1)
            condition = abs(x1 - x0) > tolerance
            x0 = x1
            step = step + 1
            if step > max_iterations:
                flag = 0
                break
        
        if flag == 1:
            self.solution = f'Root is: {x1}'
        else:
            self.solution = "Function does not diverge."

        return self.solution, self.steps
    
    def plot(self):
        f = lambda x: eval(self.equation)
        derivative = Derivative(self.equation, 'x').doit()
        f_derivative = lambda x: eval(str(derivative))

        
        # Creating Data for the Line
        x_plot = np.linspace(-100, 100, 1000)
        f2 = np.vectorize(f)
        f3 = np.vectorize(f_derivative)
        y_plot = f2(x_plot)
        
        # Plotting Function
        fig = plt.figure()
        plt.plot(self.estimate_roots,np.zeros(len(self.estimate_roots)), 'og')
        plt.plot([-100, 100],[0,0],'k')
        plt.plot(x_plot, y_plot, c='blue')
        plt.plot(x_plot, f3(x_plot), c='green')
        # plt.xlim(min([x for x in self.estimate_roots])-2, max([x for x in self.estimate_roots])+2)
        plt.xlim([-10, 10])
        plt.ylim([-2, 2])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    test_class = NewtonRaphson()
    inFunc = 'exp(x)'
    initialGuess = 0.5
    error = 0.00001
    iterations = 100
    def function(x): return eval(inFunc)
    solution, steps = test_class.getSolution(inFunc, initialGuess, error, iterations, 6)
    test_class.plot()
    print(solution)
    print(steps)
