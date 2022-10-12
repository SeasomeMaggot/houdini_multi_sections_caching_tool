from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import hou
import toolutils
import re

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 100)
        self.window.move(300, 300)
        self.window.setWindowTitle('Multi Sections Caching Tool (No $OS in file path!)')

        self.lineEdit1 = QLineEdit(self.window)
        self.lineEdit1.setPlaceholderText("start frame")
        
        self.lineEdit2 = QLineEdit(self.window)
        self.lineEdit2.setPlaceholderText("end frame")
        
        self.onlyInt = QIntValidator()
        self.onlyInt.setRange(0, 9999)
        self.lineEdit1.setValidator(self.onlyInt)
        self.lineEdit2.setValidator(self.onlyInt)
        
        self.lineEdit1.move(10, 25)
        self.lineEdit1.resize(150, 50)
        
        self.lineEdit2.move(200, 25)
        self.lineEdit2.resize(150, 50)

        self.button = QPushButton('Run', self.window)
        self.button.move(380, 35)

        self.button.clicked.connect(self.handleCalc)
#-------------UI-----------------------------

    def handleCalc(self):
    
        try:
            sf = int(self.lineEdit1.text())
            ef = int(self.lineEdit2.text())
        except:
            QMessageBox.about(self.window,
                    'Error',
                    'Set Section Number!!!'
                    )
            raise           
#------------check frame range----------------
        
        try:
            selNodes = hou.selectedNodes()
        except:
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!!!'
                    )
            raise
        
        """
        if str(selType).find('filecache') == -1:
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!!!'
                    )
            raise
           """ 

        fr = ef - sf + 1        
        sections = (ef - sf)/len(selNodes)                                           
        sr = int(fr/sections)       
                
        for n, node in enumerate(selNodes):
        
            selType = node.type()
            
            if str(selType).find('filecache') == -1:
                QMessageBox.about(self.window,
                    'Error',
                    'File cache node ONLY!!!'
                    )
                raise
            else:
                node.parmTuple('f').deleteAllKeyframes()
                node.parm('f1').set(sf+sr*n)
                node.parm('f2').set(sf+sr*(n+1)-1)
                
                if n == len(selNodes) - 1:
                    node.parm('f2').set(ef)
                
stats = Stats()
stats.window.show()
