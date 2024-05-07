from PyQt5.QtWidgets import QApplication, QMainWindow
from GUI import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())