import copy

def GaussSedial(coefficientMatrix, b, initialGuess, showSteps, relativeError):
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
            x[i] = numerator / coefficientMatrix[i][i]
            newX = x[i]
            newError = (abs(newX - oldX) / newX) * 100
            e = max(e, newError)
        
        maxNoIterations += 1

        if showSteps == True:
            print ("Iteration (", maxNoIterations, "):", "x = ", x , "And error in it is ", e)
            
    print ("Gauss Sedial Final Result : x = ", x)

# ------------------ Main program -------------------------------#
a = [
    [12, 3, -5],
    [1, 5, 3],
    [3, 7, 13]
    ]
    
b = [1, 28, 76]
initialGuess = [1, 0, 1]
GaussSedial(a, b, initialGuess, True, 0.8)