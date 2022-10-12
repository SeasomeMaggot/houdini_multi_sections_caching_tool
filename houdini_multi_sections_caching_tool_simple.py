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
        self.window.setWindowTitle('Multi Sections Caching Tool')

        self.lineEdit = QLineEdit(self.window)
        self.lineEdit.setPlaceholderText("Input section number (Warning: No $OS in file path!)")
        self.onlyInt = QIntValidator()
        self.onlyInt.setRange(0, 9999)
        self.lineEdit.setValidator(self.onlyInt)

        self.lineEdit.move(10, 25)
        self.lineEdit.resize(300, 50)

        self.button = QPushButton('Run', self.window)
        self.button.move(380, 35)

        self.button.clicked.connect(self.handleCalc)
#-------------UI-----------------------------

    def handleCalc(self):
    
        try:
            sections = int(self.lineEdit.text())
        except:
            QMessageBox.about(self.window,
                    'Error',
                    'Set Section Number!!!'
                    )
            raise           
#------------check frame range----------------
        
        try:
            selNode = hou.selectedNodes()[0]
        except:
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!!!'
                    )
            raise
            
        selType = selNode.type()
        parent = selNode.parent()
        
        if str(selType).find('filecache') == -1:
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!!!'
                    )
            raise
            
#------------eval selected type---------------        
        elif selNode.parm('trange').eval() == 0:
             QMessageBox.about(self.window,
                    'Error',
                    'Set Frame Range!!!'
                    )
#------------check frame range----------------
                
        else:
                               
            sf = selNode.parm('f1').eval()
            ef = selNode.parm('f2').eval()
            fr = ef - sf + 1
            sr = int(fr/sections)
            
            path = selNode.parm('file').unexpandedString()
            
            upNode = selNode.input(0)
            
            subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
            subNode.setColor(hou.Color(0,0,0))            
            input = subNode.path()+'/1'
            subNode.moveToGoodPosition()
            subNode.setInput(0,upNode)                       

            
            for n in range(sections):            
                fileNode = subNode.createNode('filecache')
                fileNode.parm('filemethod').set(1)
                fileNode.setName('TMP_multi_caching_tool_section'+str(n))
                fileNode.moveToGoodPosition()
                fileNode.setInput(0,hou.item(input))                    
                fileNode.parm('file').set(path)
                fileNode.parmTuple('f').deleteAllKeyframes()
                
                if n == 0:
                    fileNode.parm('f1').set(sf+(sections-1)*sr)
                    fileNode.parm('f2').set(ef)
                else:
                    fileNode.parm('f1').set(sf+sr*(n-1))
                    fileNode.parm('f2').set(sf+sr*n-1)
            
                
stats = Stats()
stats.window.show()
