import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from operations.GaussElimination import GaussElimination
from operations.GaussJordan import GaussJordan
from operations.GaussSeidel import GaussSeidel
from operations.Jacobi import JacobiIteration

TITLE = 'Matrix Calculator'

temp_cache = ''
class Calculator(QWidget):
   def __init__(self, parent=None):
      super(Calculator, self).__init__(parent)
      self.setFixedSize(620, 520)
      self.setWindowTitle(TITLE)
      self.setWindowIcon(QIcon('src/icon.png'))
   
      # Data Storage
      self.PREV_MATRICES = []
      self.DEFAULT_PRECISION = 5

      # Main Layouts
      self.layout_main, self.tab_layout, self.layout_matrices, self.layout_matrices, self.layout_buttons, self.layout_result = QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout(), QGridLayout()

      # Tabs Widget
      self.tabs = QTabWidget()
      tabstylesheet = '''
         QTabBar::tab:selected {background: gray;}
         QTabBar::tab {padding: 5px; background: lightgray; font-weight: bold; margin-right: 5px; width: 123px; height:20px;}
         QTabBar::tab:hover {background: darkgrey;}
         QTabBar::tab:disabled {background: #e8eaed;}
      '''
      self.tabs.setStyleSheet(tabstylesheet)
      self.tab_main, self.tab_solution, self.tab_steps = QTabWidget(), QTabWidget(), QTabWidget()
      self.tabs.addTab(self.tab_main, 'Main')
      self.tabs.addTab(self.tab_solution, 'Solution')
      self.tabs.addTab(self.tab_steps, 'Solution Steps')
      # self.tab_solution.setEnabled(False)
      # self.tab_steps.setEnabled(False)

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
      self.tree_recent_matrices.itemClicked.connect(self.loadMatrix)

      # MatrixA Widget Contents
      self.lbl_matrixA = QLabel("Matrix")
      self.lbl_matrixA_X1 = QLabel("X")
      self.lbl_matrixA_X1.setAlignment(Qt.AlignCenter)
      self.lbl_matrixA.setAlignment(Qt.AlignCenter)
      self.combo_matrixA_X = QComboBox()
      self.combo_matrixA_Y = QComboBox()
      self.combo_matrixA_X.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
      self.combo_matrixA_Y.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
      self.combo_matrixA_X.setCurrentText('3')
      self.combo_matrixA_Y.setCurrentText('3')
      self.widget_matrix_A = QWidget(self)
      self.layout_matrix_A = QGridLayout()
      self.widget_matrix_A.setLayout(self.layout_matrix_A)
      self.textboxes_matrix_A = []
      for rows in range(10):
         cols = []
         for columns in range(10):
            textbox = QLineEdit(str(0))
            # textbox.setInputMask("9999")
            textbox.setAlignment(Qt.AlignCenter)
            cols.append(textbox)
            self.layout_matrix_A.addWidget(textbox, rows, columns)
         self.textboxes_matrix_A.append(cols)
      self.changeMatrixSize()
      self.layout_matrices.addWidget(self.widget_matrix_A, 2, 0, 1, 5)

      self.layout_matrices.addWidget(self.lbl_matrixA, 0, 2)
      self.layout_matrices.addWidget(self.combo_matrixA_X, 1, 1)
      self.layout_matrices.addWidget(self.lbl_matrixA_X1, 1, 2)
      self.layout_matrices.addWidget(self.combo_matrixA_Y, 1, 3)

      # Button Widget Contents
      self.btn_clear_matrix = QPushButton("Clear Matrix")
      self.btn_clear_matrix.clicked.connect(self.clearMatrix)
      self.btn_clear_matrix.setStyleSheet('QPushButton {color: red;}')
      self.btn_GaussElimination = QPushButton('Gauss Elimination')
      self.btn_GaussJordan = QPushButton('Gauss Jordan')
      self.btn_LUDecomposition = QPushButton('LU Decomposition')
      self.btn_GaussSeidel = QPushButton('Gauss Seidel')
      self.btn_JacobiIteration = QPushButton('Jacobi Iteration')
      
      self.btn_LUDecomposition.setEnabled(False)
      self.btn_GaussSeidel.setEnabled(False)
      self.btn_JacobiIteration.setEnabled(False)

      # Variables
      self.combo_LUDecomposition = QComboBox()
      self.combo_LUDecomposition.addItems(['Choose LU Method', 'Downlittle Form', 'Crout Form', 'Cholesky Form'])
      self.txt_InitialGuess = QLineEdit()
      self.txt_Cond_NumberOfIterations = QLineEdit()
      self.txt_Cond_Tolerance = QLineEdit()
      self.txt_InitialGuess.setPlaceholderText('Initial Guess')
      self.txt_Cond_NumberOfIterations.setPlaceholderText('Number of Iterations')
      self.txt_Cond_Tolerance.setPlaceholderText('Absolute Relative Error')
      self.txt_precision = QLineEdit()
      self.txt_precision.setPlaceholderText('Precision')

      self.layout_buttons.addWidget(self.txt_precision, 0, 0)
      # self.layout_buttons.addWidget(self.btn_GaussJordan, 0, 1)
      # self.layout_buttons.addWidget(self.btn_PowerMethod, 0, 2, 1, 2)
      self.layout_buttons.addWidget(self.btn_clear_matrix, 0, 4)

      self.layout_buttons.addWidget(self.btn_GaussElimination, 1, 0)
      self.layout_buttons.addWidget(self.btn_GaussJordan, 1, 1)
      self.layout_buttons.addWidget(self.btn_LUDecomposition, 1, 2, 1, 2)
      self.layout_buttons.addWidget(self.combo_LUDecomposition, 1, 4)

      self.layout_buttons.addWidget(self.txt_InitialGuess, 2, 0)
      self.layout_buttons.addWidget(self.txt_Cond_NumberOfIterations, 2, 1)
      self.layout_buttons.addWidget(self.txt_Cond_Tolerance, 2, 2)
      self.layout_buttons.addWidget(self.btn_GaussSeidel, 2, 3)
      self.layout_buttons.addWidget(self.btn_JacobiIteration, 2, 4)

      self.display('Welcome to the Matrix Calculator!')

      self.combo_matrixA_X.currentTextChanged.connect(self.changeMatrixSize)
      self.combo_matrixA_Y.currentTextChanged.connect(self.changeMatrixSize)
      self.combo_LUDecomposition.currentTextChanged.connect(self.enableButtons)
      self.txt_InitialGuess.textChanged.connect(self.enableButtons)
      self.txt_Cond_NumberOfIterations.textChanged.connect(self.enableButtons)
      self.txt_Cond_Tolerance.textChanged.connect(self.enableButtons)
      self.btn_GaussElimination.clicked.connect(lambda: self.solve('GaussElimination'))
      self.btn_GaussJordan.clicked.connect(lambda: self.solve('GaussJordan'))
      self.btn_LUDecomposition.clicked.connect(lambda: self.solve('LUDecomposition'))
      self.btn_GaussSeidel.clicked.connect(lambda: self.solve('GaussSeidel'))
      self.btn_JacobiIteration.clicked.connect(lambda: self.solve('JacobiIteration'))

   def changeMatrixSize(self, matrixX=None, matrixY=None):
      if not isinstance(matrixX, int):
         matrixX = int(self.combo_matrixA_X.currentText())
         matrixY = int(self.combo_matrixA_Y.currentText())
      for rows in range(10):
         for columns in range(10):
            self.textboxes_matrix_A[rows][columns].hide()
      for rows in range(matrixX):
         for columns in range(matrixY):
            self.textboxes_matrix_A[rows][columns].show()
      self.display('[INFO]: Matrix Size Changed to ' + str(matrixX) + 'x' + str(matrixY))
   
   def getMatrix(self):
      matrixX = int(self.combo_matrixA_X.currentText())
      matrixY = int(self.combo_matrixA_Y.currentText())
      matrix = []
      try:
         for rows in range(matrixY):
            row = []
            for col in range(matrixX):
               row.append(float(self.textboxes_matrix_A[rows][col].text()))
            matrix.append(row)
         return matrix
      except:
         self.display('[ERROR] Please make sure you fill all matrix fields with numbers')
         return None
   
   def clearMatrix(self):
      for rows in range(10):
         for col in range(10):
            self.textboxes_matrix_A[rows][col].setText('0')
      self.display('[INFO]: Matrix Cleared')
   
   def display(self, text):
      self.lbl_display.setText(text)

   def enableButtons(self):
      if self.combo_LUDecomposition.currentText() != 'Choose LU Method':
         self.btn_LUDecomposition.setEnabled(True)
      else:
         self.btn_LUDecomposition.setEnabled(False)
      
      if self.txt_InitialGuess.text() != '' and self.txt_Cond_NumberOfIterations.text() != '' and self.txt_Cond_Tolerance.text() != '':
         self.btn_GaussSeidel.setEnabled(True)
         self.btn_JacobiIteration.setEnabled(True)
      else:
         self.btn_GaussSeidel.setEnabled(False)
         self.btn_JacobiIteration.setEnabled(False)
   
   def solve(self, method):
      self.display('[PROGRESS] Getting ready to solve the matrix...')
      matrix = self.getMatrix()
      if not matrix: return
      precision = int(self.txt_precision.text()) if self.txt_precision.text() else self.DEFAULT_PRECISION
      initial_guess = float(self.txt_InitialGuess.text()) if self.txt_InitialGuess.text() else None
      number_of_iterations = int(self.txt_Cond_NumberOfIterations.text()) if self.txt_Cond_NumberOfIterations.text() else None
      tolerance = float(self.txt_Cond_Tolerance.text()) if self.txt_Cond_Tolerance.text() else None

      if method == 'GaussElimination':
         solver = GaussElimination()
         matrix = [
            [-3, 5, 2, -19],
            [5, -1, 4, -5],
            [4, -2, 2, 2]
         ]
         solution, steps = solver.getSolution(matrix)
      elif method == 'GaussJordan':
         solver = GaussJordan()
         matrix = [
            [0, 0, 3.7798654, 4],
            [10, 2, -6.78654, 2],
            [1.78654, 0, 0, 9.32]
         ]
         solution, steps = solver.getSolution(matrix, precision)
      elif method == 'LUDecomposition':
         self.display('[ERROR] LU Decomposition is not ready yet!')
         return
      elif method == 'GaussSeidel':
         solver = GaussSeidel()
         a = [
            [12, 3, -5],
            [1, 5, 3],
            [3, 7, 13]
         ]
         b = [1, 28, 76]
         initialGuess = [1, 0, 1]
         solution, steps = solver.getSolution(a, b, initialGuess, 0.8)
         
         
      elif method == 'JacobiIteration':
         solver = JacobiIteration()
         a = [
            [4, 2, 1],
            [-1, 2, 0],
            [2, 1, 4]
         ]
         b = [11, 3, 16]
         initialGuess = [1, 1, 1]
         solution, steps = solver.getSolution(a, b, initialGuess, 0.8)

      self.displaySolution(solver.operation_name, solution)
      self.displaySteps(solver.operation_name, steps)
      self.display('[INFO] Solution is ready!')
      self.saveMatrix()
   
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
      self.changeMatrixSize(matrixX=len(matrix), matrixY=len(matrix[0]))
      self.combo_matrixA_X.setCurrentText(str(len(matrix)))
      self.combo_matrixA_Y.setCurrentText(str(len(matrix[0])))
      for row_idx, row in enumerate(matrix):
         for col_idx, col in enumerate(row):
            self.textboxes_matrix_A[row_idx][col_idx].setText(str(col))
      self.display('[INFO] Matrix Loaded!')

app = QApplication(sys.argv)
ex = Calculator()
ex.show()
sys.exit(app.exec_())