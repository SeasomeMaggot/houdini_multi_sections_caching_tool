import hou

#此脚本可以自动把一个File Cache节点复制多次，提取其Frame range，分配到每一个复制的节点上，并将所有的节点挂载到后台缓存中。
#此脚本适用于CPU占用率不高，但是缓存速度却很慢的情景，如Remesh。
#不推荐将此脚本用于解算类情景



#------输入每个节点分配的帧数---------

frames = 10 #帧

#------输入每个节点分配的帧数---------



#使用前请选择一个File Cache节点，并确保它的输入端已连接
#请勿使用$OS，请勿使用Constructed路径



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
sections = int((end_frame-start_frame+1)/frames)    
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
        n.parmTuple('f').set((start_frame+i*frames,end_frame,1))
        
    else:
        n.parmTuple('f').set((start_frame+i*frames,start_frame+(i+1)*frames-1,1))
        
    n.parm('cookoutputnode').pressButton()
