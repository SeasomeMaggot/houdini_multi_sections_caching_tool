import hou

#-----------Input------------------

sections = 10

#-----------Input------------------

try:
    selNode = hou.selectedNodes()[0]
    selType = selNode.type()
    if str(selType).find('filecache') == -1:
        raise hou.Error("Select a File cache node!!!")
except:
    raise hou.Error("Select a File cache node!!!")
#------------------------------check if file cache node is selected-------------------------------
    
start_frame = selNode.parm('f1').eval()
end_frame = selNode.parm('f2').eval()
fl = int((end_frame-start_frame+1)/sections)    
#-------------------------------pick up frame # from selected node---------------------------------    

upNode = selNode.input(0)

if upNode is None:
    raise hou.Error("File cache node must have an input!!!")
    
path = selNode.parm('file').unexpandedString()
if path.find('$OS') != -1:
    raise hou.Error("No $OS!!!")
    
if selNode.parm('filemethod').eval() == 0:
    raise hou.Error("No $constructed file path!!!")
#-----------------------------raise error if node has input, uses $OS, or constructed file path-----
    
    
parent = selNode.parent()    
displayNode = selNode.parent().displayNode()
   
subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
subNode.setColor(hou.Color(0,0,0))            
input = subNode.path()+'/1'
subNode.moveToGoodPosition()
subNode.setInput(0,upNode)
#-----------------------------create subnetwork----------------------------------------------------

for i in range(sections):    
    n = subNode.copyItems((selNode,))[0]
    n.setInput(0,hou.item(input))
    n.moveToGoodPosition()
    n.parmTuple('f').deleteAllKeyframes()
    
    if i == sections -1:        
        n.parmTuple('f').set((start_frame+i*fl,end_frame,1))
        
    else:
        n.parmTuple('f').set((start_frame+i*fl,start_frame+(i+1)*fl-1,1))
        
    n.parm('cookoutputnode').pressButton()
