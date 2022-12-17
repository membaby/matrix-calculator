import copy
import numpy as np
from math import log10, floor


def round_sig(x, sig=5):
   return round(x, sig-int(floor(log10(abs(x))))-1) 

def GaussSedial(coefficientMatrix, b, initialGuess, relativeError):
    x = initialGuess
    maxNoIterations = 0
    e = relativeError
    steps = []
    while (maxNoIterations != 100 and e >= relativeError):
        e = 0
        for i in range(len(b)):
            numerator = b[i]
            for j in range(len(b)):
                if i != j:
                    numerator -= x[j]*coefficientMatrix[i][j]

            oldX = x[i]        
            x[i] = round_sig(numerator / coefficientMatrix[i][i])
            newX = x[i]
            newError = (abs(newX - oldX) / newX) * 100
            e = max(e, newError)
        
        maxNoIterations += 1

        steps.append("Iteration (" + str(maxNoIterations) + "):x = " + str(x) + " And error in it: " + str(e))
            
    return x, steps

# ------------------ Main program -------------------------------#
a = [
    [12, 3, -5],
    [1, 5, 3],
    [3, 7, 13]
    ]
    
b = [1, 28, 76]
initialGuess = [1, 0, 1]
result, steps = GaussSedial(a, b, initialGuess, 0.8)
print (result)
for i in range (len(steps)):
    print (steps[i], "\n")
