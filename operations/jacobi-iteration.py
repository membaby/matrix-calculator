class JacobiIteration:
    def __init__(self):
        self.operation_name = 'Jacobi Iteration Method'
        self.solution = []
        self.solution_steps = []
    
    def getSolution(self, input_matrix, initial_guess=0, iterations=100, tolerance=0.005):
        # WRITE SOLUTION HERE
        return self.solutions, self.solution_steps

if __name__ == '__main__':
    test_class = JacobiIteration()
    test_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    test = test_class.getSolution(test_matrix)
    print(test)