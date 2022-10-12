import hou

#-----------Input------------------

start_frame = 1
end_frame = 100

#-----------Input------------------



selNodes = hou.selectedNodes()
fl = int((end_frame-start_frame+1)/len(selNodes))

for i, n in enumerate(selNodes):
    n.parmTuple('f').deleteAllKeyframes()

    if i == len(selNodes)-1:        
        n.parmTuple('f').set((start_frame+i*fl,end_frame,1))
        
    else:
        n.parmTuple('f').set((start_frame+i*fl,start_frame+(i+1)*fl-1,1))
