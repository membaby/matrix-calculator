import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from operations.GaussElimination import GaussElimination
from operations.GaussJordan import GaussJordan
from operations.GaussSeidel import GaussSeidel
from operations.Jacobi import JacobiIteration
from operations.LUdecomposition import LUDecomposition
import time
import sympy as sp
import re

TITLE = 'Matrix Calculator'

class Calculator(QWidget):
   def __init__(self, parent=None):
      super(Calculator, self).__init__(parent)
      self.setFixedSize(620, 520)
      self.setWindowTitle(TITLE)
      self.setWindowIcon(QIcon('src/icon.png'))

      # Data Storage
      self.PREV_MATRICES = []
      self.DEFAULT_PRECISION = 6
      self.DEFAULT_MATRIX_SIZE = 3
      self.DEFAULT_INITIAL_GUESS = 0
      self.DEFAULT_ITERATIONS = 200
      self.DEFAULT_TOLERANCE = 0.005

      # Main Layouts
      self.layout_main, self.tab_layout, self.layout_matrices, self.layout_matrices, self.layout_buttons, self.layout_result = QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout()

      # Tabs Widget
      self.tabs = QTabWidget()
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

      self.txt_solution = QPlainTextEdit(self.tab_solution)
      self.txt_steps = QPlainTextEdit(self.tab_steps)
      self.txt_steps.resize(590, 500)
      self.txt_solution.resize(590, 500)
      self.txt_solution.setStyleSheet('QPlainTextEdit {font-size: 18px;}')
      self.txt_steps.setStyleSheet('QPlainTextEdit {font-size: 18px;}')
      # self.txt_solution.setEnabled(False)
      # self.txt_steps.setEnabled(False)

      self.layout_main.addWidget(self.tabs, 0, 0)
      self.tab_main.setLayout(self.tab_layout)

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
      self.combo_operation.addItems(['Gauss Elimination', 'Gauss Jordan', 'LU Decomposition', 'Gauss Seidel', 'Jacobi Iteration'])
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
      self.layout_buttons.addWidget(self.txt_Cond_NumberOfIterations, 2, 2)
      self.layout_buttons.addWidget(self.txt_Cond_Tolerance, 2, 3)
      self.layout_buttons.addWidget(self.txt_InitialGuess, 2, 4)
      # LU Decomposition Condition
      self.layout_buttons.addWidget(self.combo_LUDecomposition, 2, 3, 1, 2)
      # General
      self.layout_buttons.addWidget(self.txt_precision, 2, 0, 1, 1)
      self.layout_buttons.addWidget(self.btn_loadMatrix, 0, 5)
      self.layout_buttons.addWidget(self.btn_clear_matrix, 1, 5)
      self.layout_buttons.addWidget(self.btn_solve, 3, 0, 1, 6)

      self.combo_matrixA_X.currentTextChanged.connect(self.changeMatrixSize)
      self.combo_operation.currentTextChanged.connect(self.changeAvailableConditions)
      self.btn_solve.clicked.connect(self.solve)
      self.btn_loadMatrix.clicked.connect(self.ShowCustomFormatMatrix)

      self.changeAvailableConditions()
      self.display('Welcome to the Matrix Calculator!')
   
   def changeAvailableConditions(self):
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
         for columns in range(matrixX+1):
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
            for col in range(matrixX+1):
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
      
   def solve(self):
      try:
         start = time.time()
         self.display('[PROGRESS] Getting ready to solve the matrix...')
         matrix = self.getMatrix()
         if not matrix: return
         method = self.combo_operation.currentText()
         task = {
            'precision': int(self.txt_precision.text()) if self.txt_precision.text() else self.DEFAULT_PRECISION,
            'initial_guess': [float(x) for x in self.txt_InitialGuess.text().split(',')] if self.txt_InitialGuess.text() else [self.DEFAULT_INITIAL_GUESS for x in range(len(matrix))],
            'number_of_iterations': int(self.txt_Cond_NumberOfIterations.text()) if self.txt_Cond_NumberOfIterations.text() else self.DEFAULT_ITERATIONS,
            'tolerance': float(self.txt_Cond_Tolerance.text()) if self.txt_Cond_Tolerance.text() else self.DEFAULT_TOLERANCE,
            'scale': self.cbx_scaling.isChecked(),
            'LU-Form': self.combo_LUDecomposition.currentText()
         }

         if method == 'Gauss Elimination':
            solver = GaussElimination()
            solution, steps = solver.getSolution(matrix, task['precision'])
         elif method == 'Gauss Jordan':
            solver = GaussJordan()
            solution, steps = solver.getSolution(matrix, task['precision'])
         elif method == 'LU Decomposition':
            if task['LU-Form'] == 'Choose LU Method':
               self.display('[ERROR] Please select a LU method!')
               return
            solver = LUDecomposition()
            solution, steps = solver.getSolution(matrix, task['LU-Form'], task['precision'])

         elif method == 'Gauss Seidel':
            for i in range(len(matrix)):
               if matrix[i][i] == 0 :
                  self.display('[ERROR] Diagonal element cannot be zero!')
                  self.displaySolution('Gauss Seidel', ['There is no solution.', 'Diagonal element cannot be zero!'])
                  self.displaySteps('Gauss Seidel', ['There is no solution.', 'Diagonal element cannot be zero!'])
                  return False
            solver = GaussSeidel()
            solution, steps = solver.getSolution(matrix, task['initial_guess'], task['tolerance'], task['number_of_iterations'], task['precision'])
            
         elif method == 'Jacobi Iteration':
            for i in range(len(matrix)):
               if matrix[i][i] == 0 :
                  self.display('[ERROR] Diagonal element cannot be zero!')
                  self.displaySolution('Jacobi Iteration', ['There is no solution.', 'Diagonal element cannot be zero!'])
                  self.displaySteps('Jacobi Iteration', ['There is no solution.', 'Diagonal element cannot be zero!'])
                  return False
            solver = JacobiIteration()
            solution, steps = solver.getSolution(matrix, task['initial_guess'], task['tolerance'], task['number_of_iterations'], task['precision'])
         
         end = time.time()
         total_time = end - start

         self.displaySolution(solver.operation_name, solution)
         self.displaySteps(solver.operation_name, steps)
         self.display(f'[INFO] Solution is ready! ({total_time} seconds taken!)')
         self.saveMatrix()
      except Exception as err:
         print(err)
         self.display('[ERROR] Something went wrong! Please try again!')
   
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
      self.txt_solution.setPlainText(text)

   def clear_matrix(self):
      for rows in range(10):
         for col in range(10):
               self.textboxes_matrix_A[rows][col].setText('0')
      self.display('[INFO]: Matrix Cleared')

   def display(self, text):
      self.lbl_display.setText(text)

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
   
   def saveMatrix(self):
      matrix = self.getMatrix()
      if not matrix: return
      if matrix not in self.PREV_MATRICES:
         self.PREV_MATRICES.append(matrix)
         self.tree_recent_matrices.addTopLevelItem(QTreeWidgetItem([str(matrix)]))
   
   def loadMatrix(self, it, col):
      matrix = eval(it.text(col))
      self.changeMatrixSize(matrixX=len(matrix))
      self.combo_matrixA_X.setCurrentText(str(len(matrix)))
      for row_idx, row in enumerate(matrix):
         for col_idx, col in enumerate(row):
            self.textboxes_matrix_A[row_idx][col_idx].setText(str(col))
      self.display('[INFO] Matrix Loaded!')

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
