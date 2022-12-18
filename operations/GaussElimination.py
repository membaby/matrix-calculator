class GaussElimination:
    def __init__(self):
        self.operation_name = 'Gauss Elimination'
        self.n = 0
        self.solutions = []
        self.solution_steps = []
    
    def getSolution(self, input_matrix):
        self.n = len(input_matrix)
        self.solutions = [0 for i in range(self.n)]
        flag = self.forwardElimination(input_matrix)
        if(flag == "Have a unique solution"):
            return [round(x, 8) for x in self.solutions], self.solution_steps
        elif(flag == "Singular and have no solution"):
            return -1
        else:
            return self.infiniteNumber(input_matrix, flag), self.solution_steps
    
    def forwardElimination(self, input_matrix):
        factor = 1
        for k in range(self.n):
            self.solution_steps.append([row[:] for row in input_matrix])
            iMax = k
            vMax = input_matrix[iMax][k]
            
            for i in range(k+1, self.n):
                maxInRow = 0
                for j in range(i, self.n+1):
                    maxInRow = max(abs(input_matrix[i][j]), abs(maxInRow))

                if(abs(input_matrix[i][k]/maxInRow > vMax)):
                    vMax = input_matrix[i][k]
                    iMax = i
                    
            if not vMax:
                if(input_matrix[k][self.n] == 0):
                    return k
                else:
                    return "Singular and have no solution"
                
                
            if(iMax != k):
                for h in range(self.n+1):
                    temp = input_matrix[iMax][h]
                    input_matrix[iMax][h] = input_matrix[k][h]
                    input_matrix[k][h] = temp
                    
                self.solution_steps.append([row[:] for row in input_matrix])
                
            for i in range(k+1, self.n):
                factor = (input_matrix[i][k])/input_matrix[k][k]
                self.solution_steps.append(factor)
                input_matrix[i][k] = 0
                for j in range(k+1, self.n+1):
                    input_matrix[i][j] = round(input_matrix[i][j] - input_matrix[k][j]*factor, 8)
                        
        return "Have a unique solution"
    
    def backSubstitution(self, input_matrix):        
        for i in range(self.n-1, -1, -1):
            self.solutions[i] = input_matrix[i][self.n]
            
            for j in range(i+1, self.n):
                self.solutions[i] -= input_matrix[i][j]*self.solutions[j]
                
            self.solutions[i] = (self.solutions[i]/input_matrix[i][i])
            
    def infiniteNumber(self, input_matrix, k):
        self.solutions = []
        for i in range(self.n-k, -1, -1):
            sol = ''
            for j in range(i+1, self.n):
                sol += str(input_matrix[i][j]) + '*X' + str(j) + ' + '
            sol = sol[:len(sol)-3]
            sol += ' = ' + str(input_matrix[i][self.n])
            self.solutions.append(sol)
        return self.solutions


if __name__ == '__main__':
    test_class = GaussElimination()
    test_matrix = [
        [-3, 5, 2, -19],
        [5, -1, 4, -5],
        [4, -2, 2, 2]
    ]
    solutions, solution_steps = test_class.getSolution(test_matrix)
    print(solutions)
    print('xxxx')
    print(solution_steps)