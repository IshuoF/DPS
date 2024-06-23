from PySide6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QApplication
import sys
from ui_function import MainWindow


app = QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec()