from operations.GaussElimination import GaussElimination
from operations.GaussJordan import GaussJordan
from operations.GaussSeidel import GaussSeidel
from operations.Jacobi import JacobiIteration
from operations.LUdecomposition import LUDecomposition


class Solver:
    def get_solution(self, parent, method, matrix, task):
        solution, steps = None, None
        if method == 'Gauss Elimination':
            solver = GaussElimination()
            solution, steps = solver.getSolution(matrix, task['precision'])
        elif method == 'Gauss Jordan':
           solver = GaussJordan()
           solution, steps = solver.getSolution(matrix, task['precision'])
        elif method == 'LU Decomposition':
           if task['LU-Form'] == 'Choose LU Method':
              parent.display('[ERROR] Please select a LU method!')
              return None, None
           solver = LUDecomposition()
           solution, steps = solver.getSolution(matrix, task['LU-Form'], task['precision'])
        elif method == 'Gauss Seidel':
           for i in range(len(matrix)):
              if matrix[i][i] == 0 :
                 parent.display('[ERROR] Diagonal element cannot be zero!')
                 parent.displaySolution('Gauss Seidel', ['There is no solution.', 'Diagonal element cannot be zero!'])
                 parent.displaySteps('Gauss Seidel', ['There is no solution.', 'Diagonal element cannot be zero!'])
                 return None, None
           solver = GaussSeidel()
           solution, steps = solver.getSolution(matrix, task['initial_guess'], task['tolerance'], task['number_of_iterations'], task['precision'])
           
        elif method == 'Jacobi Iteration':
           for i in range(len(matrix)):
              if matrix[i][i] == 0 :
                 parent.display('[ERROR] Diagonal element cannot be zero!')
                 parent.displaySolution('Jacobi Iteration', ['There is no solution.', 'Diagonal element cannot be zero!'])
                 parent.displaySteps('Jacobi Iteration', ['There is no solution.', 'Diagonal element cannot be zero!'])
                 return None, None
           solver = JacobiIteration()
           solution, steps = solver.getSolution(matrix, task['initial_guess'], task['tolerance'], task['number_of_iterations'], task['precision'])
        return solution, steps