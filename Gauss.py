import copy
import numpy as np
from math import log10, floor


def round_sig(x, sig=5):
   return round(x, sig-int(floor(log10(abs(x))))-1) 

def check(coefficientMatrix):
    for i in range (len (coefficientMatrix)):
        if coefficientMatrix [i][i] == 0 :
            return False

    return True

def GaussSedial(coefficientMatrix, b, initialGuess, relativeError, MAX = 100):


    x = initialGuess
    maxNoIterations = MAX
    e = relativeError
    steps = []
    while (maxNoIterations != 0 and e >= relativeError):
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
        
        maxNoIterations -= 1

        steps.append("Iteration (" + str(MAX - maxNoIterations) + "):x = " + str(x) + " And error in it: " + str(e))
            
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


# pesoudo code for seidel

# while (maxNoIterations != 0 and e >= relativeError){ // while loop for iterations

#     for bi : (i = 1 to n){ //iteration to calculate xi
#         numerator = b[i]
#         for  xj : (j = 1 to n , j != i){ // itetation to calculate numerator
#             subtract from numerator x[j] * coefficient (corresponding coefficient)
#         }
#         x[i] = (numerator / coefficientMatrix[i][i]) // update xi
#         compute error = ((xi new - xi old) / (xi new)) * 100
#     }
# }
