import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import matplotlib.pyplot as plt
import numpy as np
from operations.solver import Solver
from operations.Bisection import Bisection
from operations.RegulaFalsi import RegulaFalsi
from operations.NewtonRaphson import NewtonRaphson
from operations.FixedPoint import FixedPoint
from operations.secant import Secant

TITLE = 'Matrix Calculator'


class Calculator(QWidget):
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.setFixedSize(700, 620)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon('src/icon.png'))

        # Data Storage
        self.PREV_MATRICES = []
        self.PREV_FUNCTIONS = []
        self.DEFAULT_PRECISION = 1000
        self.DEFAULT_MATRIX_SIZE = 3
        self.DEFAULT_INITIAL_GUESS = 0
        self.DEFAULT_ITERATIONS = 50
        self.DEFAULT_TOLERANCE = 0.00001
        self.DEFAULT_LowerBoundary = -10
        self.DEFAULT_UpperBoundary = 10
        self.DEFAULT_InitialGuess = 0
        self.DEFAULT_InitialGuess2 = 0

        # Main Layouts
        self.layout_main, self.tab_layout, self.layout_matrices, self.layout_matrices, self.layout_buttons, self.layout_result, self.layout_ops, self.layout_rootfinder = QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout()

        # Tabs Widget
        self.tabs = QTabWidget()
        self.tabs_ops = QTabWidget()
        style_sheet = '''
         QTabBar::tab:selected {background: gray;}
         QTabBar::tab {padding: 5px; background: lightgray; font-weight: bold; margin-right: 5px; width: 123px; height:20px;}
         QTabBar::tab:hover {background: darkgrey;}
         QTabBar::tab:disabled {background: #e8eaed;}
      '''
        self.tabs.setStyleSheet(style_sheet)
        self.tab_main, self.tab_solution, self.tab_steps = QTabWidget(), QTabWidget(), QTabWidget()
        self.tabs.addTab(self.tab_main, 'Main')
        self.tabs.addTab(self.tab_solution, 'Solution')
        self.tabs.addTab(self.tab_steps, 'Solution Steps')

        self.tab_matrixops, self.tab_linearops = QTabWidget(), QTabWidget()
        self.tabs_ops.addTab(self.tab_matrixops, 'Matrix Solver')
        self.tabs_ops.addTab(self.tab_linearops, 'Root Finder')

        self.tab_matrixops.setLayout(self.tab_layout)
        self.tab_linearops.setLayout(self.layout_rootfinder)

        self.txt_solution = QPlainTextEdit(self.tab_solution)
        self.txt_steps = QPlainTextEdit(self.tab_steps)
        self.txt_steps.resize(690, 550)
        self.txt_solution.resize(690, 550)
        self.txt_solution.setStyleSheet('QPlainTextEdit {font-size: 18px;}')
        self.txt_steps.setStyleSheet('QPlainTextEdit {font-size: 18px;}')
        # self.txt_solution.setEnabled(False)
        # self.txt_steps.setEnabled(False)

        self.layout_main.addWidget(self.tabs, 0, 0)
        self.tab_main.setLayout(self.layout_ops)
        self.layout_ops.addWidget(self.tabs_ops, 0, 0)

        # Root Finder
        self.lbl_display_rootfinder = QLabel('')
        self.txt_rootfinder_funciton = QLineEdit()
        self.txt_rootfinder_funciton.setPlaceholderText('F(x)')

        self.lbl_rootfinder_title = QLabel("Root Finder")
        self.lbl_rootfinder_title.setAlignment(Qt.AlignCenter)

        self.tree_rootfinder_functions = QTreeWidget()
        self.tree_rootfinder_functions.setColumnCount(1)
        self.tree_rootfinder_functions.setHeaderLabels(['Recent Functions'])
        self.tree_rootfinder_functions.itemClicked.connect(self.loadFunction)

        ## Root Finder: Buttons and Variables
        self.combo_rootfinder_method = QComboBox()
        self.combo_rootfinder_method.addItems(
            ['Bisection', 'False Position', 'Fixed Point', 'Newton Raphson', 'Secant Method'])
        self.combo_rootfinder_method.currentIndexChanged.connect(lambda x: self.changeAvailableConditions(True))
        self.txt_rootfinder_precision = QLineEdit()
        self.txt_rootfinder_EPS = QLineEdit()
        self.txt_rootfinder_MaxIterations = QLineEdit()
        self.txt_rootfinder_LowerBoundary = QLineEdit()
        self.txt_rootfinder_UpperBoundary = QLineEdit()
        self.txt_rootfinder_InitialGuess = QLineEdit()
        self.txt_rootfinder_InitialGuess2 = QLineEdit()

        self.btn_rootfinder_reset = QPushButton('Clear')
        self.btn_rootfinder_reset.setStyleSheet('QPushButton {color: red;}')
        self.btn_rootfinder_solve = QPushButton('SOLVE')
        self.btn_rootfinder_reset.clicked.connect(lambda x: self.clear_matrix(True))

        self.txt_rootfinder_precision.setPlaceholderText('Precision')
        self.txt_rootfinder_EPS.setPlaceholderText('Absolute Relative Error')
        self.txt_rootfinder_MaxIterations.setPlaceholderText('Max Iterations')
        self.txt_rootfinder_LowerBoundary.setPlaceholderText('Lower Boundary')
        self.txt_rootfinder_UpperBoundary.setPlaceholderText('Upper Boundary')
        self.txt_rootfinder_InitialGuess.setPlaceholderText('Initial Guess (X0)')
        self.txt_rootfinder_InitialGuess2.setPlaceholderText('Initial Guess (X1)')

        self.layout_rootfinder.addWidget(self.lbl_display_rootfinder, 0, 0, 1, 2)
        self.layout_rootfinder.addWidget(self.lbl_rootfinder_title, 1, 0, 1, 2)
        self.layout_rootfinder.addWidget(QLabel('Equation:'), 2, 0)
        self.layout_rootfinder.addWidget(self.txt_rootfinder_funciton, 2, 1)

        self.widget_rootfinder_buttons = QWidget(self)
        self.layout_rootfinder_buttons = QGridLayout()
        self.widget_rootfinder_buttons.setLayout(self.layout_rootfinder_buttons)

        self.layout_rootfinder_buttons.addWidget(self.combo_rootfinder_method, 0, 0, 1, 6)
        self.layout_rootfinder_buttons.addWidget(self.btn_rootfinder_reset, 0, 6)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_precision, 1, 0)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_InitialGuess, 1, 1)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_InitialGuess2, 1, 2)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_LowerBoundary, 1, 3)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_UpperBoundary, 1, 4)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_EPS, 1, 5)
        self.layout_rootfinder_buttons.addWidget(self.txt_rootfinder_MaxIterations, 1, 6)
        self.layout_rootfinder_buttons.addWidget(self.btn_rootfinder_solve, 2, 0, 1, 7)

        self.layout_rootfinder.addWidget(self.widget_rootfinder_buttons, 3, 0, 1, 2)
        self.layout_rootfinder.addWidget(self.tree_rootfinder_functions, 6, 0, 1, 2)

        self.btn_rootfinder_solve.clicked.connect(lambda x: self.solve(rootfinder=True))

        # Main Widgets
        self.widget_matrices = QWidget(self)
        self.widget_buttons = QWidget(self)
        self.widget_result = QWidget(self)

        self.setLayout(self.layout_main)
        self.widget_matrices.setLayout(self.layout_matrices)
        self.widget_buttons.setLayout(self.layout_buttons)
        self.widget_result.setLayout(self.layout_result)

        # Display Label
        self.lbl_display = QLabel("DISPLAY WARNING MESSAGES HERE")

        self.tab_layout.addWidget(self.lbl_display, 0, 0, 1, 2)
        self.tab_layout.addWidget(self.widget_matrices, 1, 0)
        self.tab_layout.addWidget(self.widget_buttons, 2, 0, 1, 2)
        self.tab_layout.addWidget(self.widget_result, 3, 0, 1, 2)
        self.tree_recent_matrices = QTreeWidget()
        self.tree_recent_matrices.setColumnCount(1)
        self.tree_recent_matrices.setHeaderLabels(['Recent Matrices'])
        self.tab_layout.addWidget(self.tree_recent_matrices, 4, 0)

        self.tree_recent_matrices.itemClicked.connect(self.loadMatrix)

        # MatrixA Widget Contents
        self.lbl_matrixA = QLabel("Matrix")
        self.lbl_matrixA_X1 = QLabel("Square Matrix Size")
        self.lbl_matrixA_X1.setAlignment(Qt.AlignCenter)
        self.lbl_matrixA.setAlignment(Qt.AlignCenter)
        self.combo_matrixA_X = QComboBox()
        self.combo_matrixA_X.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.widget_matrix_A = QWidget(self)
        self.layout_matrix_A = QGridLayout()
        self.widget_matrix_A.setLayout(self.layout_matrix_A)
        self.textboxes_matrix_A = []
        for rows in range(10):
            cols = []
            for columns in range(11):
                textbox = QLineEdit(str(0))
                textbox.setAlignment(Qt.AlignCenter)
                cols.append(textbox)
                self.layout_matrix_A.addWidget(textbox, rows, columns)
            self.textboxes_matrix_A.append(cols)
        self.changeMatrixSize(self.DEFAULT_MATRIX_SIZE)
        self.layout_matrices.addWidget(self.widget_matrix_A, 2, 0, 1, 5)

        self.layout_matrices.addWidget(self.lbl_matrixA, 0, 2)
        self.layout_matrices.addWidget(self.combo_matrixA_X, 1, 3)
        self.layout_matrices.addWidget(self.lbl_matrixA_X1, 1, 1)
        # self.layout_matrices.addWidget(self.combo_matrixA_Y, 1, 3)

        # Button Widget Contents
        self.btn_clear_matrix = QPushButton("Clear Matrix")
        self.btn_clear_matrix.clicked.connect(self.clearMatrix)
        self.btn_clear_matrix.setStyleSheet('QPushButton {color: red;}')
        self.btn_loadMatrix = QPushButton("Custom Format")

        # Variables
        self.combo_LUDecomposition = QComboBox()
        self.combo_LUDecomposition.addItems(['Choose LU Method', 'Dolittle Form', 'Crout Form', 'Cholesky Form'])
        self.combo_operation = QComboBox()
        self.combo_operation.addItems(
            ['Gauss Elimination', 'Gauss Jordan', 'LU Decomposition', 'Gauss Seidel', 'Jacobi Iteration'])
        self.txt_InitialGuess = QLineEdit()
        self.txt_Cond_NumberOfIterations = QLineEdit()
        self.txt_Cond_Tolerance = QLineEdit()
        self.txt_InitialGuess.setPlaceholderText('Initial Guess (Seperate by Comma)')
        self.txt_Cond_NumberOfIterations.setPlaceholderText('Number of Iterations')
        self.txt_Cond_Tolerance.setPlaceholderText('Absolute Relative Error')
        self.cbx_scaling = QCheckBox('Enable Scaling')
        self.cbx_scaling.setEnabled(False)
        self.txt_precision = QLineEdit()
        self.txt_precision.setPlaceholderText('Precision')
        self.btn_solve = QPushButton('Solve')

        self.layout_buttons.addWidget(self.combo_operation, 1, 0, 1, 5)
        self.layout_buttons.addWidget(self.cbx_scaling, 2, 5)
        # Gauss Seider & Jacobi Iteration Conditions
        self.layout_buttons.addWidget(self.txt_precision, 2, 0, 1, 1)
        self.layout_buttons.addWidget(self.txt_Cond_NumberOfIterations, 2, 2)
        self.layout_buttons.addWidget(self.txt_Cond_Tolerance, 2, 3)
        self.layout_buttons.addWidget(self.txt_InitialGuess, 2, 4)
        # LU Decomposition Condition
        self.layout_buttons.addWidget(self.combo_LUDecomposition, 2, 3, 1, 2)
        # General
        self.layout_buttons.addWidget(self.btn_loadMatrix, 0, 5)
        self.layout_buttons.addWidget(self.btn_clear_matrix, 1, 5)
        self.layout_buttons.addWidget(self.btn_solve, 3, 0, 1, 6)

        self.combo_matrixA_X.currentTextChanged.connect(self.changeMatrixSize)
        self.combo_operation.currentTextChanged.connect(lambda x: self.changeAvailableConditions(False))
        self.btn_solve.clicked.connect(self.solve)
        self.btn_loadMatrix.clicked.connect(self.ShowCustomFormatMatrix)

        self.changeAvailableConditions()
        self.changeAvailableConditions(True)
        self.display('Welcome to the Matrix Calculator!')

    def changeAvailableConditions(self, rootfinder=False):
        if rootfinder:
            self.txt_rootfinder_InitialGuess.setVisible(False)
            self.txt_rootfinder_InitialGuess2.setVisible(False)
            self.txt_rootfinder_LowerBoundary.setVisible(False)
            self.txt_rootfinder_UpperBoundary.setVisible(False)
            selected_option = self.combo_rootfinder_method.currentText()
            if selected_option in ['Bisection', 'False Position']:
                self.txt_rootfinder_LowerBoundary.setVisible(True)
                self.txt_rootfinder_UpperBoundary.setVisible(True)
            elif selected_option in ['Newton Raphson', 'Fixed Point']:
                self.txt_rootfinder_InitialGuess.setVisible(True)
            elif selected_option == 'Secant Method':
                self.txt_rootfinder_InitialGuess.setVisible(True)
                self.txt_rootfinder_InitialGuess2.setVisible(True)
            return

        selected_operation = self.combo_operation.currentText()
        self.combo_LUDecomposition.setVisible(False)
        self.txt_InitialGuess.setVisible(False)
        self.txt_Cond_NumberOfIterations.setVisible(False)
        self.txt_Cond_Tolerance.setVisible(False)
        if selected_operation == 'LU Decomposition':
            self.combo_LUDecomposition.setVisible(True)
        elif selected_operation == 'Gauss Seidel' or selected_operation == 'Jacobi Iteration':
            self.txt_InitialGuess.setVisible(True)
            self.txt_Cond_NumberOfIterations.setVisible(True)
            self.txt_Cond_Tolerance.setVisible(True)

    def changeMatrixSize(self, matrixX=None):
        if not isinstance(matrixX, int):
            matrixX = int(self.combo_matrixA_X.currentText())
        for rows in range(10):
            for columns in range(11):
                self.textboxes_matrix_A[rows][columns].hide()
                self.textboxes_matrix_A[rows][columns].setStyleSheet('QLineEdit {color: black;}')
        for rows in range(matrixX):
            for columns in range(matrixX + 1):
                self.textboxes_matrix_A[rows][columns].show()
                if columns == matrixX:
                    self.textboxes_matrix_A[rows][columns].setPlaceholderText('b')
                    self.textboxes_matrix_A[rows][columns].setStyleSheet('QLineEdit {color: blue;}')
        self.combo_matrixA_X.setCurrentText(str(matrixX))
        self.display('[INFO]: Matrix Size Changed to ' + str(matrixX) + 'x' + str(matrixX))

    def getMatrix(self):
        matrixX = int(self.combo_matrixA_X.currentText())
        matrix = []
        try:
            for rows in range(matrixX):
                row = []
                for col in range(matrixX + 1):
                    try:
                        row.append(float(self.textboxes_matrix_A[rows][col].text()))
                    except:
                        self.textboxes_matrix_A[rows][col].setText('0')
                        row.append(float(self.textboxes_matrix_A[rows][col].text()))
                        self.display(f'[UPDATE] Cell at ({rows}, {col}) is set to 0 because it was not a number!')
                matrix.append(row)
            return matrix
        except Exception as err:
            print(err)
            self.display('[ERROR] Please make sure you fill all matrix fields with numbers')
            return None

    def clearMatrix(self):
        for rows in range(10):
            for col in range(10):
                self.textboxes_matrix_A[rows][col].setText('0')
        self.display('[INFO]: Matrix Cleared')

    def solve(self, rootfinder=False):
        try:
            if not rootfinder:
                start = time.time()
                self.display('[PROGRESS] Getting ready to solve the matrix...')
                matrix = self.getMatrix()
                if not matrix: return
                method = self.combo_operation.currentText()
                task = {
                    'precision': int(
                        self.txt_precision.text()) if self.txt_precision.text() else self.DEFAULT_PRECISION,
                    'initial_guess': [float(x) for x in
                                      self.txt_InitialGuess.text().split(',')] if self.txt_InitialGuess.text() else [
                        self.DEFAULT_INITIAL_GUESS for x in range(len(matrix))],
                    'number_of_iterations': int(
                        self.txt_Cond_NumberOfIterations.text()) if self.txt_Cond_NumberOfIterations.text() else self.DEFAULT_ITERATIONS,
                    'tolerance': float(
                        self.txt_Cond_Tolerance.text()) if self.txt_Cond_Tolerance.text() else self.DEFAULT_TOLERANCE,
                    'scale': self.cbx_scaling.isChecked(),
                    'LU-Form': self.combo_LUDecomposition.currentText()
                }

                solver = Solver()
                solution, steps = solver.get_solution(self, method, matrix, task)

                end = time.time()
                total_time = end - start

                if solution:
                    self.displaySolution(method, solution)
                    self.displaySteps(method, steps)
                    self.display(f'[INFO] Solution is ready! ({total_time} seconds taken!)')
                    self.saveMatrix()

            else:
                start = time.time()
                self.display('[PROGRESS] Getting ready to find the roots...', rootfinder=True)
                method = self.combo_rootfinder_method.currentText()
                equation = self.txt_rootfinder_funciton.text()

                if not equation:
                    self.display('[ERROR] Please enter a function to find the roots of!', rootfinder=True)
                    return

                task = {
                    'precision': int(
                        self.txt_rootfinder_precision.text()) if self.txt_rootfinder_precision.text() else self.DEFAULT_PRECISION,
                    'tolerance': float(
                        self.txt_rootfinder_EPS.text()) if self.txt_rootfinder_EPS.text() else self.DEFAULT_TOLERANCE,
                    'number_of_iterations': int(
                        self.txt_rootfinder_MaxIterations.text()) if self.txt_rootfinder_MaxIterations.text() else self.DEFAULT_ITERATIONS,
                    'upper_boundary': float(
                        self.txt_rootfinder_UpperBoundary.text()) if self.txt_rootfinder_UpperBoundary.text() else self.DEFAULT_UpperBoundary,
                    'lower_boundary': float(
                        self.txt_rootfinder_LowerBoundary.text()) if self.txt_rootfinder_LowerBoundary.text() else self.DEFAULT_LowerBoundary,
                    'initial_guess': float(
                        self.txt_rootfinder_InitialGuess.text()) if self.txt_rootfinder_InitialGuess.text() else self.DEFAULT_InitialGuess,
                    'initial_guess_2': float(
                        self.txt_rootfinder_InitialGuess2.text()) if self.txt_rootfinder_InitialGuess2.text() else self.DEFAULT_InitialGuess,
                }

                if method == 'Bisection':
                    solver = Bisection()
                    solution, steps, estimate_roots = solver.bisection(equation, task['lower_boundary'],
                                                                       task['upper_boundary'], task['tolerance'],
                                                                       task['precision'], task['number_of_iterations'])
                    self.plot(method, equation, task, estimate_roots)

                elif method == 'False Position':
                    solver = RegulaFalsi()
                    solution, steps, estimate_roots = solver.regula_falsi(equation, task['lower_boundary'],
                                                                          task['upper_boundary'], task['tolerance'],
                                                                          task['precision'],
                                                                          task['number_of_iterations'])
                    self.plot(method, equation, task, estimate_roots)

                elif method == 'Newton Raphson':
                    solver = NewtonRaphson()
                    solution, steps = solver.getSolution(equation, task['initial_guess'], task['tolerance'],
                                                         task['number_of_iterations'], task['precision'])
                    solver.plot()

                elif method == 'Fixed Point':
                    solver = FixedPoint()
                    solution, steps, values = solver.fixed_point(equation, task['tolerance'], task['precision'],
                                                                 task['initial_guess'], task['number_of_iterations'])
                    self.plot(method, equation, task, values)

                elif method == 'Secant Method':
                    solver = Secant()
                    solution, steps = solver.SecantMethod(equation, task['initial_guess'], task['initial_guess_2'],
                                                          task['tolerance'], task['number_of_iterations'],
                                                          task['precision'])
                    solver.plot()

                end = time.time()
                total_time = end - start

                if solution:
                    self.displaySolution(method, solution)
                    self.displaySteps(method, steps)
                    self.display(f'[INFO] Solution is ready! ({total_time} seconds taken!)', rootfinder=True)
                    self.saveMatrix(rootfinder=True)

        except Exception as err:
            print(err)
            self.display('[ERROR] Something went wrong! Please try again!')

    def plot(self, method, equation, task, estimate_roots):
        x = np.linspace(task['lower_boundary'], task['upper_boundary'], 1000)
        plt.plot([-100, 100], [0, 0], 'k')  # plotting horizontal line at y=0
        print(equation)
        f = lambda x: eval(equation)
        print('OK')
        f2 = np.vectorize(f)
        if method in ['Bisection', 'False Position']:
            plt.plot(x, f2(x))  # plotting the function
            plt.plot(estimate_roots[:-1], np.zeros(len(estimate_roots) - 1), 'or')  # plotting the roots
            plt.plot(estimate_roots[-1:], np.zeros(1), 'og')  # plotting the roots
            plt.xlim(task['lower_boundary'], task['upper_boundary'])
            plt.ylim(-0.5, 3)
        elif method in ['Fixed Point']:
            xx = np.arange(0, 6, 0.1)
            plt.plot(xx, f2(xx), 'b')
            plt.plot(xx, xx, 'r')
            for x, y in estimate_roots:
                plt.plot([x, x], [x, y], 'g')
                plt.plot([x, y], [y, y], 'g')
            plt.xlim(min([x[0] for x in estimate_roots] + [task['initial_guess']]) - 2,
                     max([x[0] for x in estimate_roots] + [task['initial_guess']]) + 2)
            plt.ylim(-0.5, max([x[1] for x in estimate_roots]) + 2)

        plt.title(f'Finding Roots by {method}')
        plt.show()

    def displaySolution(self, method, solution):
        text = '>> ' + method + ' Solution:\n------------------------------------\n\n'
        if isinstance(solution, list):
            for line in solution:
                if isinstance(line, list):
                    for subline in line:
                        text += str(subline) + '\n'
                    text += '\n'
                else:
                    text += str(line) + '\n\n'
        else:
            text += '\n\n' + str(solution)
        self.txt_solution.setPlainText(text)

    def clear_matrix(self, rootfinder=False):
        if rootfinder:
            self.txt_rootfinder_funciton.setText('')
            self.txt_rootfinder_EPS.setText('')
            self.txt_rootfinder_MaxIterations.setText('')
            self.txt_rootfinder_precision.setText('')
            self.txt_rootfinder_UpperBoundary.setText('')
            self.txt_rootfinder_LowerBoundary.setText('')
            self.txt_rootfinder_InitialGuess.setText('')
            self.txt_rootfinder_InitialGuess2.setText('')
            self.display('[INFO]: Variables Cleared', rootfinder=True)
            return

        for rows in range(10):
            for col in range(10):
                self.textboxes_matrix_A[rows][col].setText('0')
        self.display('[INFO]: Matrix Cleared')

    def display(self, text, rootfinder=False):
        if not rootfinder:
            self.lbl_display.setText(text)
        else:
            self.lbl_display_rootfinder.setText(text)

    def displaySteps(self, method, steps):
        text = '>> ' + method + ' Steps:\n------------------------------------\n\n'
        if isinstance(steps, list):
            for line in steps:
                if isinstance(line, list):
                    for subline in line:
                        text += str(subline) + '\n'
                    text += '\n'
                else:
                    text += str(line) + '\n'
        self.txt_steps.setPlainText(text)

    def saveMatrix(self, rootfinder=False):
        if not rootfinder:
            matrix = self.getMatrix()
            if not matrix: return
            if matrix not in self.PREV_MATRICES:
                self.PREV_MATRICES.append(matrix)
                self.tree_recent_matrices.addTopLevelItem(QTreeWidgetItem([str(matrix)]))
        else:
            function = self.txt_rootfinder_funciton.text()
            if not function: return
            if function not in self.PREV_FUNCTIONS:
                self.PREV_FUNCTIONS.append(function)
                self.tree_rootfinder_functions.addTopLevelItem(QTreeWidgetItem([function]))

    def loadMatrix(self, it, col):
        matrix = eval(it.text(col))
        self.changeMatrixSize(matrixX=len(matrix))
        self.combo_matrixA_X.setCurrentText(str(len(matrix)))
        for row_idx, row in enumerate(matrix):
            for col_idx, col in enumerate(row):
                self.textboxes_matrix_A[row_idx][col_idx].setText(str(col))
        self.display('[INFO] Matrix Loaded!')

    def loadFunction(self, it):
        function = it.text(0)
        self.txt_rootfinder_funciton.setText(function)
        self.display('[INFO] Function Loaded!', rootfinder=True)

    def ShowCustomFormatMatrix(self):
        self.sub_window = CustomFormatMatrix()
        self.sub_window.submitClicked.connect(self.on_sub_window_confirm)
        self.sub_window.show()

    def on_sub_window_confirm(self, equations):
        matrix = []
        equations = equations.split('\n')
        for equation in equations:
            row = []
            for element in equation.split(' '):
                row.append(float(element))
            matrix.append(row)
        self.changeMatrixSize(matrixX=len(matrix))
        for row_idx, row in enumerate(matrix):
            for col_idx, col in enumerate(row):
                self.textboxes_matrix_A[row_idx][col_idx].setText(str(col))


class CustomFormatMatrix(QWidget):
    submitClicked = pyqtSignal(str)  # <-- This is the sub window's signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon('src/icon.png'))

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.line_edit = QPlainTextEdit(placeholderText="Enter Equations")
        self.btn = QPushButton("Submit")
        layout.addWidget(self.line_edit)
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.confirm)

    def confirm(self):  # <-- Here, the signal is emitted *along with the data we want*
        self.submitClicked.emit(self.line_edit.toPlainText())
        self.close()


app = QApplication(sys.argv)
ex = Calculator()
ex.show()
sys.exit(app.exec_())
