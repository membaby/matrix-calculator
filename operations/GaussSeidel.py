import copy
import numpy as np
from math import log10, floor


class GaussSeidel:
    def __init__(self):
        self.operation_name = 'Gauss Seidel Elimination'
        self.solution = []
        self.solution_steps = []
    
    def round_sig(self, x, sig=5):
        return round(x, sig-int(floor(log10(abs(x))))-1) 

    
    def getSolution(self, coefficientMatrix, b, initialGuess, relativeError):
        x = initialGuess
        maxNoIterations = 0
        e = relativeError
        while (maxNoIterations != 100 and e >= relativeError):
            e = 0
            for i in range(len(b)):
                numerator = b[i]
                for j in range(len(b)):
                    if i != j:
                        numerator -= x[j]*coefficientMatrix[i][j]

                oldX = x[i]
                x[i] = self.round_sig(numerator / coefficientMatrix[i][i])
                newX = x[i]
                newError = (abs(newX - oldX) / newX) * 100
                e = max(e, newError)
            
            maxNoIterations += 1
            text = f'Iteration [{maxNoIterations}]: X = {x} (E: {e})'
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
    b = [1, 28, 76]
    initialGuess = [1, 0, 1]
    test = test_class.getSolution(a, b, initialGuess, 0.8)
    print(test)