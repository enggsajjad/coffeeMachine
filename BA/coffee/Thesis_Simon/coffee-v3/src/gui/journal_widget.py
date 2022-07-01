import sys
import time
from subprocess import Popen, PIPE
from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QTimer
from PyQt5.Qt import QApplication

class JournalWidget(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.reader_thread = TerminalReader()
        self.reader_thread.new_line.connect(self.append_line)
        self.reader_thread.start()

    @pyqtSlot(str)
    def append_line(self, line):
        self.append(line)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

class TerminalReader(QThread):
    new_line = pyqtSignal(str)
    p = None

    def run(self):
        self.p = Popen(["/bin/journalctl", "-f", "-b", "-u", "coffee-v3.service"], bufsize=1, stdout=PIPE, text=True)
        with self.p.stdout:
            for line in iter(self.p.stdout.readline, ''):
                self.new_line.emit(line.strip())

    def exit(self):
        self.p.terminate()
        super().exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    tw = JournalWidget()
    tw.setGeometry(0, 2000, 2000, 500)
    tw.show()
    sys.exit(app.exec_())
