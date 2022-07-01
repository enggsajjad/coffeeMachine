import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import pyqtSlot, QTimer
import time

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

        timer = QTimer(self)
        timer.timeout.connect(self.blocking)
        timer.start(3000)


    def blocking(self):
        time.sleep(2)
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

def setup(conn=None):
    app = QApplication(sys.argv)
    # ex = )App()
    svgWidget = QSvgWidget('../res/lock-solid.svg')
    svgWidget.setGeometry(50,50,100,100)
    svgWidget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    setup()
