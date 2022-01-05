# This Python file uses the following encoding: utf-8
import os
import sys

from PySide6 import QtGui
from PySide6.QtGui import QTextDocument, QTextCursor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPlainTextEdit
from PySide6.QtCore import QFile, QProcess, QIODevice, QByteArray

from util import fpath


windows = []

def set_file_path(label: QLabel):
    filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    label.setText(filepath)


def append_text(text_edit: QPlainTextEdit, text: bytes):
    text_edit.moveCursor(QTextCursor.End)
    text_edit.insertPlainText(text.decode("utf-8"))
    text_edit.moveCursor(QTextCursor.End)


def test():
    window = QUiLoader().load(QFile(fpath("processwindow.ui")), None)
    window.setWindowTitle("Nao Gui Shell")
    windows.append(window)
    window.show()
    output_edit = window.processOutput
    process = QProcess()
    process.setProgram("/usr/bin/ls")
    # process.setProgram("/usr/bin/extest")
    process.setArguments(["-al"])
    process.start()
    process.readyReadStandardOutput.connect(lambda: append_text(output_edit, process.readAllStandardOutput().data()))


if __name__ == "__main__":
    app = QApplication([])
    window = QUiLoader().load(QFile(fpath("mainwindow.ui")), None)
    window.browseNaopptx.clicked.connect(lambda: set_file_path(window.naopptxPath))
    window.browseBehaviour.clicked.connect(lambda: set_file_path(window.behaviorPath))
    window.browsepptx.clicked.connect(lambda: set_file_path(window.pptxPath))
    window.runNaopptx.clicked.connect(test)
    window.setWindowTitle("Nao Gui Shell")
    # window.setGeometry(0, 0, 400, 200)
    window.show()
    sys.exit(app.exec())
