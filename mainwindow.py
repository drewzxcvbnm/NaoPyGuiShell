# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile

def fpath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



if __name__ == "__main__":
    app = QApplication([])
    window = QUiLoader().load(QFile(fpath("mainwindow.ui")), None)
    window.setWindowTitle("Nao Gui Shell")
    # window.setGeometry(0, 0, 400, 200)
    window.show()
    sys.exit(app.exec())
