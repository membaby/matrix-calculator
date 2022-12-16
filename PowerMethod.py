numberOfIterations = input("Enter Number of iterations of power method :")

vector = [1, 1, 1]
matrix = [[1, 2, 3], [5, 2, 0], [2, 4, 3]]
result = [0, 0, 0]
eigenValue = 0

for w in range(int(numberOfIterations)):
    index = 0
    for i in range(3):
        for j in range (3):
            result[index] += vector[i] * matrix[i][j]
        index += 1
        
    eigenValue = max(result)
    for it in range(3):
        result[it] /= eigenValue
    
    
print (result, eigenValue)