from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import hou

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 100)
        self.window.move(300, 300)
        self.window.setWindowTitle('Multi Sections Caching Tool')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("Input section number")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 50)

        self.button = QPushButton('Run', self.window)
        self.button.move(380, 35)

        self.button.clicked.connect(self.handleCalc)


    def handleCalc(self):
        
        selType = hou.selectedNodes()[0].type()
        if str(selType).find('filecache') == -1:
            print('fuck you!')
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!'
                    )


#------------eval selected type---------------

        
        

stats = Stats()
stats.window.show()
