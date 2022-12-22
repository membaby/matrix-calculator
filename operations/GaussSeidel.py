from math import log10, floor


class GaussSeidel:
    def __init__(self):
        self.operation_name = 'Gauss Seidel Elimination'
        self.solution = []
        self.solution_steps = []
    
    def round_sig(self, x, sig=5):
        if x == 0:
            return 0
        return round(x, sig-int(floor(log10(abs(x))))-1)

    def getSolution(self, matrix, initialGuess, relativeError, MAX, precision):
        coefficientMatrix = [x[:-1] for x in matrix]
        b = [x[-1] for x in matrix]
        x = initialGuess
        maxNoIterations = MAX
        e = relativeError
        while (maxNoIterations != 0 and e >= relativeError):
            e = 0
            for i in range(len(b)):
                numerator = b[i]
                for j in range(len(b)):
                    if i != j:
                        numerator -= x[j] * coefficientMatrix[i][j]

                oldX = x[i]
                x[i] = self.round_sig(numerator / coefficientMatrix[i][i], precision)
                newX = x[i]
                if x[i] != 0 :
                    newError = (abs(newX - oldX) / newX) * 100
                    e = max(e, newError)
            
            maxNoIterations -= 1
            text = f'Iteration [{MAX-maxNoIterations}]: X = {x[:-1]} (E: {e})'
            self.solution_steps.append(text)
        self.solution = x
        for idx in range(len(self.solution)):
            self.solution[idx] = f'X{idx} = ' + str(self.solution[idx])

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
    test = test_class.getSolution(a, bs, initialGuess, 0.8, 7)
    print(test)
