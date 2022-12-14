import hou
import tempfile
import types
import collections

def _attributes_to_string(obj, atrr_dict):
    for k, v in atrr_dict.items():
        if isinstance(v, bool) and v == True or v == None:
            obj.attributes_string += '%s '% k.upper()
        elif v == False:
            continue
        elif isinstance(v, (tuple, list)):
            v = map(str,v)
            obj.attributes_string += "%s(%s,%s) " % (k.upper(), v[0], v[1])
        else:
            obj.attributes_string += "%s(%s) " % (k.upper(), str(v))

class HBaseContainer(object):
    def __init__(self):
        self.child_list = []
        self.attributes_string = ""
        self.attributes = dict(hstretch = True)

    def addGadget(self, gadget):
        self.child_list.append(gadget)

    def addLayout(self, layout):
        self.child_list.append(layout)

    def setAttributes(self, **kwargs):
        self.attributes.update(kwargs)


class HBaseGadget(object):
    def __init__(self, name, label):
        self.name = "%s.gad" % name
        self.label = label
        self._ui_value = "%s.val" % name
        self.attributes = dict(hstretch = True)
        self.attributes_string = ""
        self.enabled = True
        self.dialog = None
        self.init_value = None
        self.callbacks = set()

    def setEnabled(self, value = True):
        self.enabled = value
        if self.dialog:
            self.dialog.enableValue(self._ui_value, value)

    def setValue(self, value):
        if self.dialog:
            self.dialog.setValue(self._ui_value, value)
        else:
            self.init_value = value


    def getValue(self):
        if self.dialog:
            return self.dialog.value(self._ui_value)
        else:
            raise ValueError('Can\'t get value for %s gadget' % self.name)

    def _set_multivalue(self, iterable):
        self.dialog.setValue(self._ui_value[0], iterable[0])
        self.dialog.setValue(self._ui_value[1], iterable[1])
        self.dialog.setValue(self._ui_value[2], iterable[2])


    def connect(self, func):
        self.callbacks.add(func)
class _HBaseMenu(HBaseGadget):
    def __init__(self, name, label, items):
        super(_HBaseMenu, self).__init__(name, label)
        self.items = items

    def menuItems(self):
        if self.dialog:
            return self.dialog.menuItems(self._ui_value)

    def setMenuItems(self, items):
        self.items = items
        if self.dialog:
            self.dialog.setMenuItems(self._ui_value, self.items)

    def menuDefString(self):
        _s = "%s = SELECT_MENU\n{\n" % self._ui_value
        for i in self.items:
            _s += '\t"%s"\n' % str(i)
        _s += "}"
        return _s

    def __repr__(self):
        return ""
        
class HRowLayout(HBaseContainer):
    def __init__(self):
        super(HRowLayout, self).__init__()

    def __repr__(self):
        _attributes_to_string(self, self.attributes)
        return 'ROW'

class HColumnLayout(HBaseContainer):
    def __init__(self):
        super(HColumnLayout, self).__init__()

    def __repr__(self):
        _attributes_to_string(self, self.attributes)
        return 'COL'

class HButton(HBaseGadget):
    def __init__(self, name, label):
        super(HButton, self).__init__(name, label)

    def setAttributes(self, **kwargs):
        try:
            # For some reason setting the look attrib on a button, makes it disappear
            del kwargs['look']
        except KeyError:
            pass
        super(HButton, self).setAttributes(**kwargs)

    def __repr__(self):
        _attributes_to_string(self, self.attributes)
        _s = "ACTION_BUTTON \"{label}\" VALUE({value}) ".format(
            label = self.label, value = self._ui_value)
        _s += self.attributes_string
        _s += ';'
        return _s


class HIconButton(HBaseGadget):
    def __init__(self, name, icon):
        super(HIconButton, self).__init__(name, "")
        self._icon = icon
        self.attributes = {"hstretch" : False}

    def setIcon(self, iconpath):
        self._icon = iconpath

    def __repr__(self):
        _attributes_to_string(self, self.attributes)
        _s = "ACTION_ICONBUTTON \"{icon}\" VALUE({value}) ".format(
            icon = self._icon, value = self._ui_value)
        _s += self.attributes_string
        _s += ';'
        return _s

class HIntSlider(HBaseGadget):
    def __init__(self, name, label, range = (1, 10), noInputField = False):
        super(HIntSlider, self).__init__(name, label)
        self.no_field = noInputField
        self.range = range

    def setRange(self, srange):
        self.range = srange

    def lockRange(self):
        self.lock_range = True

    def __repr__(self):
        _attributes_to_string(self, self.attributes)
        if self.no_field:
            slidertype = 'INT_SLIDER'
        else:
            slidertype = 'INT_SLIDER_FIELD'
        _s = "{name} = {slider} \"{label}\" VALUE({value}) {attrs} ".format(
                name = self.name, label = self.label, value = self._ui_value,
                attrs = self.attributes_string, slider = slidertype)

        if hasattr(self, 'range'):
            _s += "RANGE(%d, %d) " % (self.range[0], self.range[1])
        if hasattr(self, 'lock_range'):
            _s += "LOCK_RANGE "
        _s += ';'
        return _s

class HBaseWindow(object):
    def __init__(self, name, title):
        self.name = name
        self.type = 'WINDOW'
        self.title = title
        self._ui_value = "%s_ui.val" % name
        self.ui_str = ""
        self.attributes = dict(hstretch = True, value = self._ui_value, look = 'plain')
        self.attributes_string = ""
        self.items_list = []
        self._gadgets_flatten_list = []
        self._menu_definitions = ""
        self.dialog = None

    def _indentWrite(self, string):
        self.ui_str += " "*4 + string + '\n'

    def setWindowAttributes(self, **kwargs):
        self.attributes.update(kwargs)


    def addGadget(self, gadget):
        self.items_list.append(gadget)

    def addLayout(self, layout):
        self.items_list.append(layout)

    def setWindowLayout(self, layout):
        if layout not in ('vertical', 'horizontal', 'cell'):
            raise ValueError('Unknown layout: %s' % layout)
        self.attributes_string += "LAYOUT(%s) " % layout

    def _write_menus(self):
        ## Menus definition must be written erlier in the script
        def traverse_layout(item):
            if isinstance(item, _HBaseMenu):
                self._indentWrite(item.menuDefString())
            elif isinstance(item, HBaseContainer):
                for sub in item.child_list:
                    traverse_layout(sub)
        for item in self.items_list:
            traverse_layout(item)

    def _write_gadget(self, gadget):
        self._indentWrite(gadget.__repr__())

    def _write_layouts(self):
        _attributes_to_string(self, self.attributes)
        def traverse_layout(item):
            if isinstance(item, HBaseGadget):
                self._write_gadget(item)
                self._gadgets_flatten_list.append(item)

            elif isinstance(item, HBaseContainer):
                self._indentWrite(item.__repr__())
                self._indentWrite('{')
                self._indentWrite(item.attributes_string)
                for sub_item in item.child_list:
                    traverse_layout(sub_item)
                self._indentWrite('}\n')

        for item in self.items_list:
            traverse_layout(item)


    def _make_ui_string(self):
        _attributes_to_string(self, self.attributes)
        self.ui_str = "{name} = {dtype} \"{title}\"".format(
            name = self.name, dtype = self.type, title = self.title)
        self.ui_str += "\n{\n"
        self._indentWrite(self.attributes_string)
        self._write_menus()
        self._write_layouts()
        self.ui_str += "\n}"

    def initUI(self):
        self._make_ui_string()
        tmp_f = tempfile.mktemp(suffix ='huilib')
        with open(tmp_f, 'w') as f:
            f.write(self.ui_str)
        try:
            self.dialog = hou.ui.createDialog(tmp_f)
            self.dialog.name = self.name
        except hou.OperationFailed as e:
            print ("{a:#^50}\n{ui_str}\n{a:#^50}".format(error = e, ui_str = self.ui_str, a = '#'))
            raise e
        finally:
            from os import remove
            remove(tmp_f)

        # Pass dialog instance to gadget objects , also set Enabled/Disable attr
        for item in self._gadgets_flatten_list:
            item.dialog = self.dialog

            # Set init values
            if item.init_value:
                item.setValue(item.init_value)

            # Add callbacks
            if item.callbacks:
                for cb in item.callbacks:
                    if hasattr(cb, '__call__'):
                        if isinstance(item._ui_value, list):
                            for valuecomp in item._ui_value:
                                self.dialog.addCallback(valuecomp, cb)
                        else:
                            self.dialog.addCallback(item._ui_value, cb)


            # Set enable/disable
            try:
                item.setEnabled(item.enabled)
            except hou.OperationFailed as e:
                pass

    def show(self):
        self.dialog.setValue(self._ui_value, True)

    def close(self):
        self.dialog.setValue(self._ui_value, False)

    def _print(self):
        if not self.ui_str:
            self._make_ui_string()
        print (self.ui_str)
                
class HDialog(HBaseWindow):
    def __init__(self, name, title):
        super(HDialog, self).__init__(name, title)
        self.type = 'DIALOG'

class SimpleImportDialog(HDialog):
    def __init__(self, name, title):
        super(SimpleImportDialog, self).__init__(name, title)
        self.setWindowLayout('vertical')
        self.setWindowAttributes(stretch = True, margin = 0.1, spacing = 0.1, min_width = 5)
        
        # Column Layout
        col = HColumnLayout()
        
        self.slider1 = HIntSlider('slider1', 'Frames')
        self.slider1.setRange((1,50))
        self.slider1.setValue(10)
        self.slider1.lockRange()
        

        # Buttons in row Layout
        self.importButton = HButton('import', 'Run')
        self.closeButton = HButton('close', 'Close')
        row = HRowLayout()
        row.addGadget(self.importButton)
        row.addGadget(self.closeButton)

        # Add file field and buttons raw layout
        col.addGadget(self.slider1)
        col.addLayout(row)

        # Connect button signals
        self.closeButton.connect(self.close)
        self.importButton.connect(self.cb_import)
        self.addLayout(col)

        # This method should ALWAYS be called last!
        self.initUI()


    def cb_import(self):
        
        frames = self.slider1.getValue()
        
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
        sections = int((end_frame-start_frame+1)/frames+1)    
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
        
        subNode.setName('DeleteThisAfterFinish')    
        

ui = SimpleImportDialog(name = 'import_dlg', title = 'Import Dialog')
ui.show()
