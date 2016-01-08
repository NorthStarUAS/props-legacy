"""

props.py: a property tree system for python

Provides a hierarchical tree of shared data values.
 - Modules can use this tree as a way to share data
   (i.e. communicate) in a loosly structure / flexible way.
 - Both reader and writer can create properties in the shared tree as they
   need them so there is less worry about initialization order dependence.
 - Tree values can be accessed in native python code as nested class
   members: a = root; a.b.c.var1 = 42
 - Children nodes can be enumerated: /sensors/gps[0], /sensors/gps[1], etc.
 - C++ interface allows complex but flexible data sharing between mixed
   C++ and python modules.
 - Maps well to xml or json data storage (i.e. xml/json config files can
   be loaded into a subtree (child) in the root shared property tree.

Notes:
 - getChild(path, True) will create 'path' as a tree of PropertyNodes() if
   it doens't exist (including any intermediate nodes.)   If the final
   component of the path is intended to be a leaf node, don't include it
   in the path or it will be created as a branch.
 - To create /path/to/variable and assign if a value, call:
   node = getNode("/path/to", create=True)
   node.variable = value

"""

import os.path
import re
import sys
import xml.etree.ElementTree as ET

class PropertyNode:
    def getChild(self, path, create=False):
        if path[:1] == '/':
            # require relative paths
            return None
        tokens = path.split('/');
        print "tokens:", tokens
        node = self
        for i, token in enumerate(tokens):
            # test for enumerated form: ident[index]
            parts = re.split('([\w-]+)\[(\d+)\]', token)
            if len(parts) == 4:
                token = parts[1]
                index = int(parts[2])
            else:
                index = None
            if token in node.__dict__:
                # node exists
                if index == None:
                    # non-enumerated node
                    node = node.__dict__[token]
                else:
                    # enumerated (list) node
                    tmp = node.__dict__[token]
                    if type(tmp) is list and len(tmp) > index:
                        node = tmp[index]
                    elif create:
                        # base node exists, but list is not large enough and
                        # create flag requested: extend the list
                        self.__extendEnumeratedNode(tmp, index)
                        node = tmp[index]
                    else:
                        return None
                if not isinstance(node, PropertyNode):
                    print "path includes leaf nodes, sorry"
                    return None
            elif create:
                # node not found and create flag is true
                if index == None:
                    node.__dict__[token] = PropertyNode()
                    node = node.__dict__[token]
                else:
                    # create node list and extend size as needed
                    node.__dict__[token] = []
                    tmp = node.__dict__[token]
                    self.__extendEnumeratedNode(tmp, index)
                    node = tmp[index]
            else:
                # requested node not found
                return None
        # return the last child node in the path
        return node

    def pretty_print(self, indent=""):
        for child in self.__dict__:
            node = self.__dict__[child]
            if isinstance(node, PropertyNode):
                print indent + "/" + child
                node.pretty_print(indent + "  ")
            elif type(node) is list:
                for i, ele in enumerate(node):
                    print indent + "/" + child + "[" + str(i) + "]:"
                    ele.pretty_print(indent + "  ")
            else:
                print indent + str(child) + ":",
                print str(node)
        
    def __extendEnumeratedNode(self, node, index):
        for i in range(len(node), index+1):
            print "appending:", i
            node.append( PropertyNode() )
            
        
root = PropertyNode()

# return/create a node relative to the shared root property node
def getNode(path, create=False):
    if path[:1] != '/':
        # require leading /
        return None
    elif path == "/":
        # catch trivial case
        return root
    print "getchild on", path[1:], "relative to root"
    return root.getChild(path[1:], create)

# internal xml tree parsing routine
def _parseXML(pynode, xmlnode, basepath):
    if len(xmlnode):
        # has children
        pynode.__dict__[xmlnode.tag] = PropertyNode()
        for child in xmlnode:
            _parseXML(pynode.__dict__[xmlnode.tag], child, basepath)
    else:
        if 'include' in xmlnode.attrib:
            pynode.__dict__[xmlnode.tag] = PropertyNode()
            filename = basepath + '/' + xmlnode.attrib['include']
            readXML(filename, pynode.__dict__[xmlnode.tag])
        else:
            # leaf
            pynode.__dict__[xmlnode.tag] = xmlnode.text
        
# load xml file and create a property tree rooted at the given node
# supports <mytag include="relative_file_path.xml" />
def readXML(filename, pynode):
    try:
        xml = ET.parse(filename)
    except:
        print filename + ": xml parse error:\n" + str(sys.exc_info()[1])
        return

    path = os.path.dirname(filename)
    print "path:", path
    xmlroot = xml.getroot()
    for child in xmlroot:
        _parseXML(pynode, child, path)
    root.pretty_print()
