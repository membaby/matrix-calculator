import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TITLE = 'Matrix Calculator'

temp_cache = ''
class Calculator(QWidget):
   def __init__(self, parent=None):
      super(Calculator, self).__init__(parent)
      self.setFixedSize(620, 520)
      self.setWindowTitle(TITLE)
      self.setWindowIcon(QIcon('src/icon.png'))

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
      self.tab_solution.setEnabled(False)
      self.tab_steps.setEnabled(False)

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
      self.lbl_matrixA_X1 = QLabel("X")
      self.lbl_matrixA_X1.setAlignment(Qt.AlignCenter)
      self.lbl_matrixA.setAlignment(Qt.AlignCenter)
      self.combo_matrixA_X = QComboBox()
      self.combo_matrixA_Y = QComboBox()
      self.combo_matrixA_X.addItems(['6', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
      self.combo_matrixA_Y.addItems(['6', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
      self.widget_matrix_A = QWidget(self)
      self.layout_matrix_A = QGridLayout()
      self.widget_matrix_A.setLayout(self.layout_matrix_A)
      self.textboxes_matrix_A = []
      for rows in range(6):
         cols = []
         for columns in range(6):
            textbox = QLineEdit(str(columns))
            textbox.setAlignment(Qt.AlignCenter)
            cols.append(textbox)
            self.layout_matrix_A.addWidget(textbox, rows, columns)
         self.textboxes_matrix_A.append(cols)
      self.layout_matrices.addWidget(self.widget_matrix_A, 2, 0, 1, 5)
      self.btn_clear_matrixA = QPushButton("Clear")

      self.layout_matrices.addWidget(self.lbl_matrixA, 0, 2)
      self.layout_matrices.addWidget(self.combo_matrixA_X, 1, 1)
      self.layout_matrices.addWidget(self.lbl_matrixA_X1, 1, 2)
      self.layout_matrices.addWidget(self.combo_matrixA_Y, 1, 3)
      # self.layout_matrices.addWidget(self.btn_clear_matrixA, 3, 4)

      # Button Widget Contents
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

      self.layout_buttons.addWidget(self.btn_GaussElimination, 0, 0)
      self.layout_buttons.addWidget(self.btn_GaussJordan, 0, 1)
      self.layout_buttons.addWidget(self.btn_LUDecomposition, 0, 2, 1, 2)
      self.layout_buttons.addWidget(self.combo_LUDecomposition, 0, 4)

      self.layout_buttons.addWidget(self.txt_InitialGuess, 1, 0)
      self.layout_buttons.addWidget(self.txt_Cond_NumberOfIterations, 1, 1)
      self.layout_buttons.addWidget(self.txt_Cond_Tolerance, 1, 2)
      self.layout_buttons.addWidget(self.btn_GaussSeidel, 1, 3)
      self.layout_buttons.addWidget(self.btn_JacobiIteration, 1, 4)

      # # MatrixA Widget
      # self.matrixA_layout = QGridLayout()
      # self.matrixA_ = QWidget()
      # self.matrixA_.setLayout(self.matrixA_layout)
      # self.matrixA = QLineEdit()
      # self.matrixA.setPlaceholderText('Matrix A')
      # self.matrixA_layout.addWidget(self.matrixA, 0, 0, 1, 2)

      # # MatrixB Widget
      # self.matrixB_layout = QGridLayout()
      # self.matrixB_ = QWidget()
      # self.matrixB_.setLayout(self.matrixB_layout)
      # self.matrixB = QLineEdit()
      # self.matrixB.setPlaceholderText('Matrix B')
      # self.matrixB_layout.addWidget(self.matrixB, 0, 0, 1, 2)


      # self.layout.addWidget(self.display, 0, 0, 1, 2)
      # self.layout.addWidget(self.matrixA_, 1, 0)
      # self.layout.addWidget(self.matrixB_, 1, 1)
      
      # # Button Widgets
      # self.btn_1 = QPushButton("1")
      # self.btn_2 = QPushButton("2")
      # self.btn_3 = QPushButton("3")
      # self.btn_4 = QPushButton("4")
      # self.btn_5 = QPushButton("5")
      # self.btn_6 = QPushButton("6")
      # self.btn_7 = QPushButton("7")

      # # Matrix A Widgets
      

      # # Tree Widget
      # self.panel = QTreeWidget()
      # self.panel.setColumnCount(5)
      # self.panel.setHeaderLabels(['ID', 'Scraper', 'Status', 'Schedule', 'Last Run'])
      # self.panel.setColumnWidth(0, 25)
      # self.panel.setColumnWidth(1, 175)
      # self.panel.setColumnWidth(2, 100)
      # self.panel.setColumnWidth(3, 100)
      # self.panel.setColumnWidth(4, 100)

      # # Label Widgets
      # self.lbl_PERFORMANCE = QLabel('CPU: 0 - RAM: 0')
      # self.lbl_PROGRESS = QLabel('Nothing is Running')

      # grid.addWidget(self.panel, 2, 0, 9, 1)

      # grid.addWidget(self.btn_START, 3, 2)
      # grid.addWidget(self.btn_STOP, 4, 2)
      # grid.addWidget(self.btn_SCHEDULE, 5, 2)
      # grid.addWidget(self.btn_LOGS, 6, 2)
      # grid.addWidget(self.btn_ADD, 7, 2)
      # grid.addWidget(self.btn_REM, 8, 2)
      # grid.addWidget(self.btn_CLOSE, 10, 2)



app = QApplication(sys.argv)
ex = Calculator()
ex.show()
sys.exit(app.exec_())