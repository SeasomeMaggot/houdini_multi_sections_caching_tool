# houdini_multi_sections_caching_tool

This tool can duplicate multiple nodes from a selected File Cache node and separate the frame range into multiple 
sections for each instances so you can cache the sections parallelly. 
This tool is usefully for the nodes that only use single thread such as remesh.

# Instruction:
Copy the script to the python source editor. change the 'sections' to any interger you want. Then, select a File Cache node (No $OS in file path, No constructed file path, filecache node must have an input). Then click the apply button and the script will run.
