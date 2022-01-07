from PySide6.QtCore import QProcess, QFile
from PySide6.QtGui import QTextCursor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPlainTextEdit

from mainwindow import windows
from util import fpath


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


def get_naopptx_process():
    root_window = windows[0]
    process = QProcess()
    process.setProgram(root_window.naopptxPath.text())
    process.setArguments(get_args(root_window))
    return process


def get_behaviour_process():
    root_window = windows[0]
    process = QProcess()
    process.setProgram(root_window.behaviourPath.text())
    process.setArguments(["--ip", root_window.naoip.text()])
    return process


def run_process(qprocess_supplier):
    window = QUiLoader().load(QFile(fpath("processwindow.ui")), None)
    window.setWindowTitle("Nao Gui Shell")
    windows.append(window)
    window.show()
    output_edit = window.processOutput
    process = qprocess_supplier()
    process.finished.connect(lambda: append_text(output_edit, f"\nProcess exited with code {process.exitCode()}"))
    process.start()
    window.killButton.clicked.connect(lambda: process.kill())
    append_text(output_edit, f'> {process.program()} {" ".join(process.arguments())}\n\n')
    process.readyRead.connect(lambda: append_text(output_edit, process.readAll().data()))
    process.readyReadStandardError.connect(lambda: append_text(output_edit, process.readAllStandardError().data()))
