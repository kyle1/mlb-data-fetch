import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton, QWidget, QMainWindow)

TIME_LIMIT = 100

class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count +=1
            time.sleep(1)
            self.countChanged.emit(count)

class Actions(object):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button results in the start of a timer and
    updates the progress bar.
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        #self.setWindowTitle('Progress Bar')
        # Main window
        MainWindow = QMainWindow()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MLB Data Fetch", "MLB Data Fetch"))

        self.progress = QProgressBar(self.centralwidget)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self.centralwidget)
        self.button.move(0, 30)
        MainWindow.show()

        self.button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        self.calc = External()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def onCountChanged(self, value):
        self.progress.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    sys.exit(app.exec_())