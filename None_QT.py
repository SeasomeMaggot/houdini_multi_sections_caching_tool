import hou

#-----------Input------------------

sections = 

#-----------Input------------------




start_frame = 1
end_frame = 100

selNode = hou.selectedNodes()[0]



fl = int((end_frame-start_frame+1)/sections)



try:
    selNode = hou.selectedNodes()[0]
    selType = selNode.type()
    if str(selType).find('filecache') == -1:
        raise hou.Error("Select a File cache node!!!")
except:
    raise hou.Error("Select a File cache node!!!")
    
parent = selNode.parent()    
displayNode = selNode.parent().displayNode()
   
subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
subNode.setColor(hou.Color(0,0,0))            
input = subNode.path()+'/1'
subNode.moveToGoodPosition()
subNode.setInput(0,upNode)

for i in range(sections):
    
    n = hou.
    n.parmTuple('f').deleteAllKeyframes()

    if i == sections -1:        
        n.parmTuple('f').set((start_frame+i*fl,end_frame,1))
        
    else:
        n.parmTuple('f').set((start_frame+i*fl,start_frame+(i+1)*fl-1,1))import hou

#-----------Input------------------

sections = 

#-----------Input------------------




start_frame = 1
end_frame = 100

selNode = hou.selectedNodes()[0]



fl = int((end_frame-start_frame+1)/sections)



try:
    selNode = hou.selectedNodes()[0]
    selType = selNode.type()
    if str(selType).find('filecache') == -1:
        raise hou.Error("Select a File cache node!!!")
except:
    raise hou.Error("Select a File cache node!!!")
    
parent = selNode.parent()    
displayNode = selNode.parent().displayNode()
   
subNode = parent.createNode('subnet','TMP_multi_caching_tool_subnet')
subNode.setColor(hou.Color(0,0,0))            
input = subNode.path()+'/1'
subNode.moveToGoodPosition()
subNode.setInput(0,upNode)

for i in range(sections):
    
    n = hou.
    n.parmTuple('f').deleteAllKeyframes()

    if i == sections -1:        
        n.parmTuple('f').set((start_frame+i*fl,end_frame,1))
        
    else:
        n.parmTuple('f').set((start_frame+i*fl,start_frame+(i+1)*fl-1,1))
