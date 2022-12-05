class GaussJordan:
    def __init__(self):
        self.operation_name = 'Gauss Jordan Eliminaiton'
        self.solution = []
        self.solution_steps = []
    
    def getSolution(self, input_matrix):
        # WRITE SOLUTION HERE
        return self.solutions, self.solution_steps


if __name__ == '__main__':
    test_class = GaussJordan()
    test_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    test = test_class.getSolution(test_matrix)
    print(test)