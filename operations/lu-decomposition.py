class LUDecomposition:
    def __init__(self):
        self.operation_name = 'Gauss Elimination'
        self.solution = []
        self.solution_steps = []
    
    def getSolution(self, input_matrix, form):
        # WRITE SOLUTION HERE
        return self.solutions, self.solution_steps

if __name__ == '__main__':
    test_class = LUDecomposition()
    test_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    test = test_class.getSolution(test_matrix, 'downlittle')
    print(test)
    test = test_class.getSolution(test_matrix, 'crout')
    print(test)
    test = test_class.getSolution(test_matrix, 'cholesky')
    print(test)