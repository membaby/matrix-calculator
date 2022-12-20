import copy
import numpy as np
from math import log10, floor


def round_sig(x, sig=5):
   return round(x, sig-int(floor(log10(abs(x))))-1) 

def Jacobi(coefficientMatrix, b, initialGuess, relativeError, MAX=100):
    temp = copy.deepcopy(initialGuess)
    x = copy.deepcopy(initialGuess)
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
            temp[i] = round_sig(numerator / coefficientMatrix[i][i])

        #take e after each iterartion 
        for i in range(len(b)):
            newError = (abs(temp[i]-x[i]) / temp[i]) * 100
            e = max(e, newError)

        # after end of each iteration take a copy to x
        x = copy.deepcopy(temp)

        maxNoIterations -= 1

        steps.append("Iteration (" + str(MAX - maxNoIterations) + "):x = " + str(x) + " And error in it: " + str(e))
         
    return x, steps

# ------------------ Main program -------------------------------#
a = [
    [4, 2, 1],
    [-1, 2, 0],
    [2, 1, 4]
    ]
    
b = [11, 3, 16]
initialGuess = [1, 1, 1]
result, steps = Jacobi(a, b, initialGuess, 0.1)
print (result)
for i in range (len(steps)):
    print (steps[i], "\n")


# pesoudo code for Jacobi

# while (maxNoIterations != 0 and e >= relativeError){ // while loop for iterations
#     tempArray[];
#     for bi : (i = 1 to n){ //iteration to calculate tempArray[i]
#         numerator = b[i]
#         for  xj : (j = 1 to n , j != i){ // itetation to calculate numerator
#             subtract from numerator x[j] * coefficient (corresponding coefficient)
#         }
#         tempArray[i] = (numerator / coefficientMatrix[i][i]) // update tempArray[i]
#     }
    
#     for xi : (i = 1 to n){ 
#         compute error = ((tempArray[i] - x[i]) / (tempArray[i])) * 100
#     }
#     x = tempArray // update x
# }