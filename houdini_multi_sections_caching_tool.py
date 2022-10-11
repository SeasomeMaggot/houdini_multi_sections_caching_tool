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
    
        sections = int(self.lineEdit.text())
        
        selNode = hou.selectedNodes()[0]
        selType = selNode.type()
        parent = selNode.parent()
        
        if str(selType).find('filecache') == -1:
            QMessageBox.about(self.window,
                    'Error',
                    'Select a File Cache Node!!!'
                    )
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
            sr = fr/sections
            
        for n in range(sections):       
            copyNode = parent.copyItems((selNode,))[0]
            copyNode.setName('TMP_multi_caching_tool_section'+str(n))
            copyNode.parmTuple('f').deleteAllKeyframes()
            copyNode.moveToGoodPosition()
            copyNode.parm('tpostrender').set(1)
            copyNode.parm('lpostrender').set(1)
            copyNode.parm('postrender').set()
            
            if n == 0:
                copyNode.setParms({'f1':(sections-1)*sr+1,})
                copyNode.setName('TMP_multi_caching_tool_section'+str(sections))
                
            else:
                copyNode.setParms({'f1':sf+sr*(n-1),'f2':sf+sr*n-1})

        
        

stats = Stats()
stats.window.show()
