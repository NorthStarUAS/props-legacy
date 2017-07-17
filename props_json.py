# TODO: properly handle enumerated nodes

import json
import os.path
import sys
import re

from props import PropertyNode, root

def mydecode(value):
    print 'mydecode:', type(value), value
    # test for int
    if type(value) is int or type(value) is float:
        return value
    result = re.match('[-+]?\d+', value)
    if result and result.group(0) == value:
        #print 'int:', value
        return int(value)
    # test for float
    result = re.match('[-+]?\d*\.\d+', value)
    if result and result.group(0) == value:
        #print 'float:', value
        return float(value)
    # test for bool
    if value == 'True' or value == 'true':
        return True
    elif value == 'False' or value == 'false':
        return False
    # otherwise return the value as a string
    return str(value)
     
# internal dict() tree parsing routine
def parseDict(pynode, newdict, basepath):
    if 'include' in newdict:
        # include file handling before anything else (follow up
        # entries implicitely overwrite the include file values.)
        if re.match('^/', newdict['include']):
            file = newdict['include']
        else:
            file = os.path.join(basepath, newdict['include'])
        # print 'include:', file
        load(file, pynode)
    for tag in newdict:
        # print tag, type(newdict[tag])
        if type(newdict[tag]) is dict:
            if not tag in pynode.__dict__:
                node = PropertyNode()
                pynode.__dict__[tag] = node
            else:
                node = pynode.__dict__[tag]
            parseDict(node, newdict[tag], basepath)
        elif type(newdict[tag]) is list:
            if tag in pynode.__dict__:
                # print 'tag exists:', type(pynode.__dict__[tag])
                if type(pynode.__dict__[tag]) is list:
                    pass
                else:
                    # promote single node to enumerated
                    pynode.__dict__[tag] = [ pynode.__dict__[tag] ]
            else:
                pynode.__dict__[tag] = []
            for i, ele in enumerate(newdict[tag]):
                if type(ele) is dict:
                    if i < len(pynode.__dict__[tag]):
                        newnode = pynode.__dict__[tag][i]
                    else:
                        newnode = PropertyNode()
                        pynode.__dict__[tag].append(newnode)
                    parseDict(newnode, ele, basepath)
                else:
                    pynode.__dict__[tag].append(mydecode(ele))
        elif type(newdict[tag]) is unicode:
            if tag == 'include':
                # already handled
                pass
            else:
                # normal case
                #print 'normal case:', tag, newdict[tag]
                mydecode(newdict[tag])
                pynode.__dict__[tag] = mydecode(newdict[tag])
        else:
            print 'json parse skipping:', tag, type(newdict[tag])
                
# load a json file and create a property tree rooted at the given node
# supports "mytag": "include=relative_file_path.json"
def load(filename, pynode):
    print "loading:", filename
    path = os.path.dirname(filename)
    try:
        f = open(filename, 'r')
        stream = f.read()
        f.close()
    except:
        print filename + ": json load error:\n" + str(sys.exc_info()[1])
        return False
    return loads(stream, pynode, path)

# load a json file and create a property tree rooted at the given node
# supports "mytag": "include=relative_file_path.json"
def loads(stream, pynode, path):
    try:
        stream = re.sub('\s*//.*\n', '\n', stream)
        newdict = json.loads(stream)
    except:
        print "json load error:\n" + str(sys.exc_info()[1])
        return False
    parseDict(pynode, newdict, path)
    return True

def buildDict(root, pynode):
    for child in pynode.__dict__:
        # print child
        node = pynode.__dict__[child]
        if isinstance(node, PropertyNode):
            root[child] = dict()
            buildDict(root[child], node)
        elif type(node) is list:
            root[child] = []
            for i, ele in enumerate(node):
                if isinstance(ele, PropertyNode):
                    newdict = dict()
                    root[child].append( newdict )
                    buildDict(newdict, ele)
                else:
                    root[child].append(str(ele))
   
        elif type(child) is str or type(child) is unicode:
            root[child] = str(node)
        else:
            print "json build skipping:", child, ":", str(node), type(child)
        
# save the property tree starting at pynode into a json xml file.
def save(filename, pynode=root):
    root = dict()
    buildDict(root, pynode)
    try:
        f = open(filename, 'w')
        json.dump(root, f, indent=4, sort_keys=True)
        f.close()
    except:
        print filename + ": json save error:\n" + str(sys.exc_info()[1])
        return
