# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile

if __name__ == "__main__":
    app = QApplication([])
    window = QUiLoader().load(QFile("mainwindow.ui"), None)
    window.setWindowTitle("Nao Gui Shell")
    # window.setGeometry(0, 0, 400, 200)
    window.show()
    sys.exit(app.exec())
