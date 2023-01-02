from math import *
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

class Secant:

    def round_sig(self, sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
        
    def SecantMethod(self, equation, x0, x1, tolerance, max_iterations, precision):
        self.equation = equation
        func = lambda x: eval(equation)
        iter = 1
        self.steps = []
        self.estimate_roots = [x0, x1]
        self.lines = []

        while True:
            fx0 = self.round_sig(precision, func(x0))
            fx1 = self.round_sig(precision, func(x1))
            if fx0 == fx1:
                self.solution = 'Unable to solve equaiton\n\n> Divison by zero'
                self.steps = ['Unable to solve equaiton\n\n> Divison by zero']
                break
            x0 = self.round_sig(precision, x0)
            x1 = self.round_sig(precision, x1)
            x2 = self.round_sig(precision, x1 - ((x0-x1)*fx1)/(fx0-fx1))
            self.lines.append((fx0, fx1))
            self.estimate_roots.append(x2)

            error = (x2 - x1) / x2
            self.steps.append(f'Iteration #{iter} (E: {round(error*100, 4)}%)\n> Xi-1 = {x0} | Xi = {x1}\n> f(Xi-1) = {fx0} | f(Xi) = {fx1}\n> Xi+1 = {x2} | f(Xi+1) = {func(x2)}\n')
            x0 = x1
            x1 = x2
            iter += 1
            
            if (iter > max_iterations or abs(error) < tolerance):
                self.solution = ('The Root is: %0.8f' % x2)
                self.solution = f'The root is {x2}'
                break

        return self.solution, self.steps
    
    def plot(self):
        f = lambda x: eval(self.equation)
        derivative = Derivative(self.equation, 'x').doit()
        f_derivative = lambda x: eval(str(derivative))

        
        # Creating Data for the Line
        x_plot = np.linspace(-100, 100, 1000)
        y_plot = f(x_plot)
        
        # Plotting Function
        fig = plt.figure()
        plt.plot(self.estimate_roots,np.zeros(len(self.estimate_roots)), 'og')
        plt.plot([-100, 100],[0,0],'k')
        plt.plot(x_plot, y_plot, c='blue')
        plt.plot(x_plot, f_derivative(x_plot), c='orange')
        # for x, y in self.lines:
        #     plt.plot([x, x], [x, y], 'g')
        #     plt.plot([x, y], [y, y], 'g')
        plt.xlim([-10, 10])
        plt.ylim([-2, 2])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()
        

if __name__ == '__main__':
    temp = Secant()
    equation = 'x ** 2 - 2'
    temp.SecantMethod(equation, 2, 3, 0.00001, 10, 8)
    temp.plot()
    # equation, x0, x1, tolerance, max_iterations, precision
    
    for step in temp.steps:
        print(step)
        
    print(temp.solution)