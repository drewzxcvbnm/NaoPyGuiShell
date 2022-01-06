# This Python file uses the following encoding: utf-8
import os
import re
import sys

from PySide6.QtGui import QTextCursor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QPlainTextEdit
from PySide6.QtCore import QFile, QProcess

from util import fpath

windows = []


def enable_run_naopptx():
    window = windows[0]
    if '/' not in window.naopptxPath.text():
        window.runNaopptx.setEnabled(False)
        return
    if '/' not in window.pptxPath.text():
        window.runNaopptx.setEnabled(False)
        return
    if re.fullmatch(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', window.naoip.text()) is None:
        window.runNaopptx.setEnabled(False)
        return
    window.runNaopptx.setEnabled(True)


def set_file_path(label: QLabel):
    filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    label.setText(filepath)
    enable_run_naopptx()


def append_text(text_edit: QPlainTextEdit, text):
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    text_edit.moveCursor(QTextCursor.End)
    text_edit.insertPlainText(text)
    text_edit.moveCursor(QTextCursor.End)


def get_args(root_window):
    args = ["--pr", root_window.pptxPath.text(), "--ip", root_window.naoip.text()]
    if root_window.noInet.isChecked():
        args.append("--no-inet")
    return args


def run_naopptx():
    root_window = windows[0]
    window = QUiLoader().load(QFile(fpath("processwindow.ui")), None)
    window.setWindowTitle("Nao Gui Shell")
    windows.append(window)
    window.show()
    output_edit = window.processOutput
    process = QProcess()
    process.setProgram(root_window.naopptxPath.text())
    process.setArguments(get_args(root_window))
    process.finished.connect(lambda: append_text(output_edit, f"\nProcess exited with code {process.exitCode()}"))
    process.start()
    window.killButton.clicked.connect(lambda: process.kill())
    append_text(output_edit, f'> {process.program()} {" ".join(process.arguments())}\n\n')
    process.readyRead.connect(lambda: append_text(output_edit, process.readAll().data()))
    process.readyReadStandardError.connect(lambda: append_text(output_edit, process.readAllStandardError().data()))


if __name__ == "__main__":
    app = QApplication([])
    window = QUiLoader().load(QFile(fpath("mainwindow.ui")), None)
    windows.append(window)
    window.naoip.textChanged.connect(enable_run_naopptx)
    window.browseNaopptx.clicked.connect(lambda: set_file_path(window.naopptxPath))
    window.browseBehaviour.clicked.connect(lambda: set_file_path(window.behaviorPath))
    window.browsepptx.clicked.connect(lambda: set_file_path(window.pptxPath))
    window.runNaopptx.clicked.connect(run_naopptx)
    window.setWindowTitle("Nao Gui Shell")
    window.show()
    sys.exit(app.exec())
