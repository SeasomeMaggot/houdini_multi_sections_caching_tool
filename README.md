# houdini_multi_sections_caching_tool

This tool can duplicate multiple nodes from a selected File Cache node and separate the frame range into multiple 
sections for each instances so you can cache the sections parallelly. 
This tool is usefully for the nodes that only use single thread such as remesh.

To use this tool, simple create a shelf tool and copy the codes into the script tap. Select a File Cache node with Frame Range on.
Then click the tool, and input the section number you want, and click the run button.
