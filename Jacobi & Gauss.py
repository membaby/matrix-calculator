import copy

numberOfIterations = input("Enter Number of iterations :")

def Jacobi(a, b, initialGuess, numberOfIterations, showSteps):
    temp = copy.deepcopy(initialGuess)
    x = copy.deepcopy(initialGuess)
    for it in range (int(numberOfIterations)):
        for i in range(3):
            numerator = b[i]
            for j in range(3):
                if i == j:
                    continue
                else:
                    numerator -= x[j]*a[i][j]
            temp[i] = numerator / a[i][i]
        x = copy.deepcopy(temp)
        if showSteps == True:
            print ("Iteration (", it+1, "):", "x = ", x)
            
    print ("Jacobi Final Result : x = ", x)
#########################################################
def GaussSedial(a, b, initialGuess, numberOfIterations, showSteps):
    x = initialGuess
    for it in range (int(numberOfIterations)):
        for i in range(3):
            numerator = b[i]
            for j in range(3):
                if i == j:
                    continue
                else:
                    numerator -= x[j]*a[i][j]
            x[i] = numerator / a[i][i]
        if showSteps == True:
            print ("Iteration (", it+1, "):", "x = ", x)
            
    print ("Gauss Sedial Final Result : x = ", x)


a = [[3, 2, 1], [1, 5, 3], [3, 4, 12]]
b = [2, 3, 4]
initialGuess = [0, 0, 0]
Jacobi(a, b, initialGuess, numberOfIterations, True)
print("----------------------------------------------------")
GaussSedial(a, b, initialGuess, numberOfIterations, True)





