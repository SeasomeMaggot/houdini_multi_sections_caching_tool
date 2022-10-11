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
        elif sections is None:
             QMessageBox.about(self.window,
                    'Error',
                    'Set Section Number!!!'
                    )
                
        else:
            sf = selNode.parm('f1').eval()
            ef = selNode.parm('f2').eval()
            fr = ef - sf + 1
            sr = fr/sections
            
            path = selNode.parm('file').unexpandedString()
            
            subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
            subNode.setColor(hou.Color(0,0,0))            
            input = subNode.path()+'/1'
            subNode.moveToGoodPosition()
            
            ropList = []
            
            for n in range(sections):
            
                copyNode = subNode.createNode('rop_geometry')
                copyNode.setName('TMP_multi_caching_tool_section'+str(n))
                copyNode.parm('trange').set(1)
                copyNode.parmTuple('f').deleteAllKeyframes()
                copyNode.moveToGoodPosition()
                copyNode.setInput(0,hou.item(input))
                
                ropList.append(copyNode)
#-----------------create instances-------------------------------------
    
                if n == 0:
                    copyNode.setParms({'f1':(sections-1)*sr+1,})
                    copyNode.setName('TMP_multi_caching_tool_section'+str(sections))
                    
                else:
                    copyNode.setParms({'f1':sf+sr*(n-1),'f2':sf+sr*n-1})
                    
            
    
            for i in ropList:
                i.parm('executebackground').pressButton()
        

stats = Stats()
stats.window.show()
