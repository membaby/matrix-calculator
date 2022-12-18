import numpy as np

class GaussJordan:
    
    def __init__(self):
        self.operation_name = 'Gauss Jordan Eliminaiton'
        self.solution = []
        self.solution_steps = []
    
    def partialPivoting(self, input_matrix, b, rows, curr):
        # find the pivot row
        pivot = curr
        for i in range(curr + 1, rows):
            # just comparing values
            if abs(input_matrix[i][curr]) > abs(input_matrix[pivot][curr]):
                pivot = i

        # swap the rows
        if pivot != curr:
            tmp = input_matrix[curr]
            input_matrix[curr] = input_matrix[pivot]
            input_matrix[pivot] = tmp
            augTmp = b[curr]
            b[curr] = b[pivot]
            b[pivot] = augTmp



    def checkRank(self, input_matrix):
        rank = np.linalg.matrix_rank(input_matrix)
        return rank


    def getSolution(self, input_matrix, precision):
        print(precision)
        rankAugA = self.checkRank(input_matrix) # rank of augmented matrix
        rows = len(input_matrix)
        columns = len(input_matrix[0]) - 1 # last column is the augmented matrix      
        b = [input_matrix[i][columns]for i in range(columns)]  #set the last column as b

        # extract the b part from input matrix
        for i in range(rows):
            input_matrix[i] = input_matrix[i][0:columns]

        rankA = self.checkRank(input_matrix); # rank of matrix 


        # check if the system has one solution, infinite solutions or no solution
        if rankA < rankAugA:
            return 'No solution'
        elif rankA == rankAugA: 
            if rankA < columns:
                return 'Infinite solutions'   

        #forward elimination
        for i in range(rows):
            self.partialPivoting(input_matrix, b, rows, i)    
            self.solution_steps.append([row[:] for row in input_matrix])         
            for j in range(i + 1, columns):
                multiplier = input_matrix[j][i] / input_matrix[i][i]
                for k in range(i, columns):
                    input_matrix[j][k] = round(input_matrix[j][k] - multiplier * input_matrix[i][k], precision if precision else 8)
                b[j] = round(b[j] - multiplier * b[i], precision if precision else 8)


        # backward elimination
        for i in range(rows - 1, -1, -1):
            self.solution_steps.append([row[:] for row in input_matrix])    
            for j in range(i - 1, -1, -1):
                multiplier = input_matrix[j][i] / input_matrix[i][i]    
                for k in range(i, columns):
                    input_matrix[j][k] = round(input_matrix[j][k] - multiplier * input_matrix[i][k], precision if precision else 8)
                b[j] = round(b[j] - multiplier * b[i], precision if precision else 8)



        # get the solution
        for i in range(rows - 1 , -1, -1):
            b[i] = round(b[i] / input_matrix[i][i], precision if precision else 8)
            input_matrix[i][i] = input_matrix[i][i] / input_matrix[i][i]
            x = round(b[i] / input_matrix[i][i], precision if precision else 8)
            self.solution.append(x)
    
        return self.solution_steps , [round(x, precision if precision else 8) for x in self.solution]

if __name__ == '__main__':
    test_class = GaussJordan()
    test_matrix = [
        [0, 0, 3.7798654, 4],
        [10, 2, -6.78654, 2],
        [1.78654, 0, 0, 9.32]
    ]
    test = test_class.getSolution(test_matrix, precision=6)
    print(test)