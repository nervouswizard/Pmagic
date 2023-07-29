from PyQt6 import QtWidgets
from gui.controller.main_ctrl import MainWindow_controller
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())