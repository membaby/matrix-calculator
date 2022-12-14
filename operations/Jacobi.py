import copy
from math import log10, floor


class JacobiIteration:
    def __init__(self):
        self.operation_name = 'Jacobi Iteration Method'
        self.solution = []
        self.solution_steps = []
    
    @staticmethod
    def round_sig(x, sig=5):
        if x == 0:
            return 0
        return round(x, sig-int(floor(log10(abs(x))))-1)

    def getSolution(self, matrix, initialGuess, relativeError, MAX, precision):
        coefficientMatrix = [x[:-1] for x in matrix]
        b = [x[-1] for x in matrix]
        temp = copy.deepcopy(initialGuess)
        x = copy.deepcopy(initialGuess)
        maxNoIterations = MAX
        e = relativeError

        while maxNoIterations != 0 and e >= relativeError:
            e = 0
            for i in range(len(b)):
                numerator = b[i]
                for j in range(len(b)):
                    if i != j:
                        numerator -= x[j]*coefficientMatrix[i][j]
                temp[i] = self.round_sig(numerator / coefficientMatrix[i][i], precision)

            # take e after each iteration
            for i in range(len(b)):
                if temp[i] != 0:
                    newError = (abs(temp[i]-x[i]) / abs(temp[i])) * 100
                    e = max(e, newError)

            # after end of each iteration take a copy to x
            x = copy.deepcopy(temp)

            maxNoIterations -= 1
            text = f'Iteration [{MAX - maxNoIterations}]: X = {x} (E: {e})'
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
    test = test_class.getSolution(a, bs, initialGuess, 0.8, 10)
    print(test)
