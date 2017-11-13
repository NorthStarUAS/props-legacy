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

import re

root = {}

def setRoot(node):
    #global root
    #root = node
    for tag in root.keys():
        del root[tag]
    for tag in node:
        root[tag] = node[tag]
    print root
    
def hasChild(node, name):
    return name in node

def getChild(start_node, path, create=False):
    print "getChild(" + path + ") create=" + str(create)
    if path.startswith('/'):
        # require relative paths
        print "Error: attempt to get child with absolute path name"
        return None
    print 'ok1'
    if path.endswith('/'):
        # we will strip this, but let's complain loudly because the
        # caller is being sloppy.
        print "WARNING: a sloppy coder has used a trailing / in a path:", path
        path = path[:-1]
    print 'ok2:', path, type(path)
    # prog = re.compile('-')
    # if prog.match(str(path)):
    #     # require valid python variable names in path
    #     print "Error: attempt to use '-' in property name"
    #     return None
    print 'ok3'
    print 'path:', path
    tokens = path.split('/');
    print "tokens:", tokens
    node = start_node
    for i, token in enumerate(tokens):
        print '  token:', token
        if False:
            # test for enumerated form: ident[index]
            parts = re.split('([\w-]+)\[(\d+)\]', token)
            if len(parts) == 4:
                token = parts[1]
                index = int(parts[2])
            else:
                index = None
        else:
            index = None
            parts = token.split('[')
            print 'parts1:', parts
            if len(parts) > 1:
                token = parts[0]
                parts = parts[1].split(']')
                print 'parts2:', parts
                if len(parts) > 1:
                    index = int(parts[0])
            else:
                index = None
        print 'ok4'
        if token in node:
            print "node exists:", token
            # node exists
            child = node[token]
            child_type = type(child)
            #print "type =", str(child_type)
            if index == None:
                if not child_type is list:
                    # requested non-indexed node, and node is not indexed
                    node = node[token]
                else:
                    # node is indexed use the first element
                    node = node[token][0]
            else:
                #print "requesting enumerated node"
                # enumerated (list) node
                if child_type is list and len(child) > index:
                    node = child[index]
                elif create:
                    if child_type is list:
                        # list is not large enough and create flag
                        # requested: extend the list
                        extendEnumeratedNode(child, index)
                    else:
                        # create on enumerated node, but not a
                        # list yet
                        save = child
                        node[token] = [save]
                        child = node[token]
                        extendEnumeratedNode(child, index)
                    node = child[index]
                else:
                    print 'returning None, no create flag given'
                    return None
            if type(node) is dict or type(node) is list:
                # ok
                pass
            else:
                print "path:", token, "includes leaf nodes, sorry"
                return None
        elif create:
            print 'node not found and create flag is true'
            if index == None:
                node[token] = {}
                node = node[token]
            else:
                # create node list and extend size as needed
                node[token] = []
                extendEnumeratedNode(node[token], index)
                node = node[token][index]
            print 'ok5'
        else:
            print 'node not found ...'
            # requested node not found
            return None
    # return the last child node in the path
    print 'ok6'
    print 'getChild():', node
    return node

def isEnum(self, child):
    if child in self.__dict__:
        if type(self.__dict__[child]) is list:
            return True
    return False

def getLen(node, child):
    if child in node:
        if type(node[child]) is list:
            return len(node[child])
        else:
            print "WARNING in getLen() path:", child, " is not enumerated"
            return 1
    else:
        print "WARNING: request length of non-existant attribute:", child
    return 0

# make the specified node enumerated (if needed) and expand the
# length (if needed)
def setLen(node, child, size, init_val=None):
    #print "called setLen()", child, size
    if child in node:
        if not type(node[child]) is list:
            # convert existing element to element[0]
            print "converting:", child, "to enumerated"
            save = node[child]
            node[child] = [save]
    else:
        #print "creating:", child
        node[child] = []
    if init_val == None:
        #print "extending branch nodes:", size
        extendEnumeratedNode(node[child], size-1)
    else:
        #print "extending leaf nodes:", size
        extendEnumeratedLeaf(node[child], size-1, init_val)

# return a list of children (attributes)
def getChildren(node, expand=True):
    result = []
    if node != None:
        # constructed the unexpanded list
        pass1 = []
        for child in node:
            pass1.append(child)
        # sort the pass1 list and expand if requested
        for child in sorted(pass1):
            if expand and type(node[child]) is list:
                for i in range(0, len(node[child])):
                    name = child + '[' + str(i) + ']'
                    result.append(name)
            else:
                result.append(child)    
    return result

def isLeaf(node, tag):
    if tag in node:
        return not type(node[tag]) is dict
    else:
        return False

def getFloat(self, name):
    if name in self.__dict__:
        return float(self.__dict__[name])
    else:
        return 0.0

def getInt(self, name):
    if name in self.__dict__:
        return int(self.__dict__[name])
    else:
        return 0

def getBool(self, name):
    if name in self.__dict__:
        return bool(self.__dict__[name])
    else:
        return False

def getString(self, name):
    if name in self.__dict__:
        return str(self.__dict__[name])
    else:
        return ""

def getFloatEnum(self, name, index):
    if name in self.__dict__:
        self.extendEnumeratedNode(self.__dict__[name], index)
        return float(self.__dict__[name][index])
    else:
        return 0.0

def getIntEnum(self, name, index):
    if name in self.__dict__:
        self.extendEnumeratedNode(self.__dict__[name], index)
        return int(self.__dict__[name][index])
    else:
        return 0.0

def getStringEnum(self, name, index):
    if name in self.__dict__:
        self.extendEnumeratedNode(self.__dict__[name], index)
        return str(self.__dict__[name][index])
    else:
        return ""

def setFloat(self, name, val):
    self.__dict__[name] = float(val)

def setInt(self, name, val):
    self.__dict__[name] = int(val)

def setBool(self, name, val):
    self.__dict__[name] = bool(val)

def setString(self, name, val):
    self.__dict__[name] = str(val)

def setFloatEnum(self, name, index, val):
    if not name in self.__dict__:
        self.setLen(name, index, 0.0)            
    self.extendEnumeratedNode(self.__dict__[name], index)
    self.__dict__[name][index] = val

def setIntEnum(self, name, index, val):
    if not name in self.__dict__:
        self.setLen(name, index, 0)            
    self.extendEnumeratedNode(self.__dict__[name], index)
    self.__dict__[name][index] = int(val)

def setBoolEnum(self, name, index, val):
    if not name in self.__dict__:
        self.setLen(name, index, 0)            
    self.extendEnumeratedNode(self.__dict__[name], index)
    self.__dict__[name][index] = bool(val)

def setStringEnum(self, name, index, val):
    if not name in self.__dict__:
        self.setLen(name, index, 0)            
    self.extendEnumeratedNode(self.__dict__[name], index)
    self.__dict__[name][index] = str(val)

def pretty_print(start_node, indent=""):
    for child in start_node:
        node = start_node[child]
        if type(node) is dict:
            print indent + "/" + child
            pretty_print(node, indent + "  ")
        elif type(node) is list:
            #print "child is list:", str(node)
            for i, ele in enumerate(node):
                # print i, str(ele)
                if type(ele) is dict:
                    print indent + "/" + child + "[" + str(i) + "]:"
                    pretty_print(ele, indent + "  ")
                else:
                    print indent + str(child) + "[" + str(i) + "]:",
                    print str(ele)
        else:
            print indent + str(child) + ":",
            print str(node)

def extendEnumeratedNode(node, index):
    for i in range(len(node), index+1):
        # print "branch appending:", i
        node.append( {} )

def extendEnumeratedLeaf(node, index, init_val):
    for i in range(len(node), index+1):
        # print "leaf appending:", i, "=", init_val
        node.append( init_val )

# return/create a node relative to the shared root property node
def getNode(path, create=False):
    print "getNode(" + path + ") create=" + str(create)
    if path[:1] != '/':
        # require leading /
        print "Error: getNode() requires a full path name"
        return None
    elif path == "/":
        # catch trivial case
        return root
    return getChild(root, path[1:], create)
