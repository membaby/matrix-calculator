import copy

def Jacobi(coefficientMatrix, b, initialGuess, showSteps, relativeError):
    temp = copy.deepcopy(initialGuess)
    x = copy.deepcopy(initialGuess)
    maxNoIterations = 0
    e = relativeError
    while (maxNoIterations != 100 and e >= relativeError):
        e = 0
        for i in range(len(b)):
            numerator = b[i]
            for j in range(len(b)):
                if i != j:
                    numerator -= x[j]*coefficientMatrix[i][j]
            temp[i] = numerator / coefficientMatrix[i][i]

        #take e after each iterartion 
        for i in range(len(b)):
            newError = (abs(temp[i]-x[i]) / temp[i]) * 100
            e = max(e, newError)

        # after end of each iteration take a copy to x
        x = copy.deepcopy(temp)

        maxNoIterations += 1

        if showSteps == True:
            print ("Iteration (", maxNoIterations, "):", "x = ", x , "And error in it is ", e)
         
    print ("Jacobi Final Result : x = ", x)

# ------------------ Main program -------------------------------#
a = [
    [4, 2, 1],
    [-1, 2, 0],
    [2, 1, 4]
    ]
    
b = [11, 3, 16]
initialGuess = [1, 1, 1]
Jacobi(a, b, initialGuess, True, 0.1)