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
            
            ret = QMessageBox.question(self.window,
                    'Mod',
                    'Add a section for mod frame?'
                    )
            if ret == QMessageBox.Yes:
                keepMod = 0
            else:
                keepMod = 1
#---------------ask if add a section for mod frames----------            
                    

                    
            sf = selNode.parm('f1').eval()
            ef = selNode.parm('f2').eval()
            fr = ef - sf + 1
            sr = int(fr/sections)
            
            path = selNode.parm('file').unexpandedString()
            
            upNode = selNode.input(0)
            
            displayNode = selNode.parent().displayNode()
            
            subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
            subNode.setColor(hou.Color(0,0,0))            
            input = subNode.path()+'/1'
            subNode.moveToGoodPosition()
            subNode.setInput(0,upNode)
            
            mergeNode = subNode.createNode('merge')
            mergeNode.moveToGoodPosition()
            
            visNode = subNode.createNode('visibility')
            visNode.moveToGoodPosition()    
            visNode.setInput(0,mergeNode)
            visNode.setDisplayFlag(1)
            
            subNode.setDisplayFlag(1)

            
            for n in range(sections+keepMod):
            
                fileNode = subNode.createNode('file')
                fileNode.setName('TMP_multi_caching_tool_section'+str(n))
                fileNode.moveToGoodPosition()
                fileNode.setInput(0,hou.item(input))                    
                fileNode.parm('filemode').set(2)
                fileNode.parm('file').set(path)            
                
                timeNode = subNode.createNode('timeshift')
                timeNode.setName('TMP_multi_caching_tool_timeshift'+str(n))
                timeNode.setInput(0,fileNode)
                timeNode.parm('frame').deleteAllKeyframes()
                timeNode.parm('frame').setExpression('$F+'+str(n*sr))
                    
                mergeNode.setInput(n,timeNode)
    
#-----------------create instances-------------------------------------                
            flipbookSettingStash = toolutils.sceneViewer().flipbookSettings().stash()
            flipbookSettingStash.sessionLabel('tmp')
            flipbookSettingStash.frameRange((sf, sf+sr-1))
            toolutils.sceneViewer().flipbook(settings = flipbookSettingStash)
            
            subNode.destroy()
            displayNode.setDisplayFlag(1)        

            
            
stats = Stats()
stats.window.show()
