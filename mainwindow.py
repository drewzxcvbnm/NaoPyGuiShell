# This Python file uses the following encoding: utf-8
import os
import re
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel
from PySide6.QtCore import QFile

from util import fpath

windows = []
IP_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'


def enable_run_naopptx():
    window = windows[0]
    if '/' not in window.naopptxPath.text():
        window.runNaopptx.setEnabled(False)
        return
    if '/' not in window.pptxPath.text():
        window.runNaopptx.setEnabled(False)
        return
    if re.fullmatch(IP_REGEX, window.naoip.text()) is None:
        window.runNaopptx.setEnabled(False)
        return
    window.runNaopptx.setEnabled(True)


def enable_run_behaviour():
    window = windows[0]
    if '/' not in window.behaviourPath.text():
        window.runBehaviour.setEnabled(False)
        return
    if re.fullmatch(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', window.naoip.text()) is None:
        window.runBehaviour.setEnabled(False)
        return
    window.runBehaviour.setEnabled(True)


def set_file_path(label: QLabel):
    filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    label.setText(filepath)
    enable_run_naopptx()
    enable_run_behaviour()


if __name__ == "__main__":
    from process import run_process, get_naopptx_process, get_behaviour_process

    app = QApplication([])
    window = QUiLoader().load(QFile(fpath("mainwindow.ui")), None)
    windows.append(window)
    window.naoip.textChanged.connect(enable_run_naopptx)
    window.naoip.textChanged.connect(enable_run_behaviour)
    window.browseNaopptx.clicked.connect(lambda: set_file_path(window.naopptxPath))
    window.browseBehaviour.clicked.connect(lambda: set_file_path(window.behaviourPath))
    window.browsepptx.clicked.connect(lambda: set_file_path(window.pptxPath))
    window.runNaopptx.clicked.connect(lambda: run_process(get_naopptx_process))
    window.runBehaviour.clicked.connect(lambda: run_process(get_behaviour_process))
    window.setWindowTitle("Nao Gui Shell")
    window.show()
    sys.exit(app.exec())
