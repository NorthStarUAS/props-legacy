# TODO: properly handle enumerated nodes

import json
import os.path
import sys
import re

from props import root, pretty_print

# recursive overlay of two dictionaries (for overriding includes trees
# in json)
def overlayDict(base, overlay):
    print 'base:', base
    print 'overlay:', overlay
    for tag in overlay:
        if type(overlay[tag]) is dict:
            if tag in base:
                overlayDict(base[tag], overlay[tag])
            else:
                base[tag] = overlay[tag]
        elif type(overlay[tag]) is list:
            for i in range(len(overlay[tag])):
                if type(overlay[tag][i]) is dict:
                    overlayDict(base[tag][i], overlay[tag][i])
                else:
                    base[tag][i] = overlay[tag][i]
        else:
            base[tag] = overlay[tag]
    
# internal dict() tree parsing routine
def parseDict(newdict, basepath):
    if 'include' in newdict:
        # include file handling before anything else (note that any
        # follow up entries implicitely overwrite the include file
        # values.)
        if re.match('^/', newdict['include']):
            file = newdict['include']
        else:
            file = os.path.join(basepath, newdict['include'])
        # print 'include:', file
        include = load(file)
        overlayDict(include, newdict)
        print 'pretty', file
        pretty_print(include)
        for tag in include:
            newdict[tag] = include[tag]
        del newdict['include']
    for tag in newdict:
        # print tag, type(newdict[tag])
        if type(newdict[tag]) is dict:
            parseDict(newdict[tag], basepath)
        elif type(newdict[tag]) is list:
            for i, ele in enumerate(newdict[tag]):
                if type(ele) is dict:
                    parseDict(ele, basepath)
                
# load a json file and create a property tree rooted at the given node
# supports "mytag": "include=relative_file_path.json"
def load(filename):
    print "loading:", filename
    path = os.path.dirname(filename)
    #try:
    f = open(filename, 'r')
    stream = f.read()
    f.close()
    #except:
    #    print filename + ": json load error:\n" + str(sys.exc_info()[1])
    #    return False
    return loads(stream, path)

# load a json file and create a property tree rooted at the given node
# supports "mytag": "include=relative_file_path.json"
def loads(stream, path):
    #try:
    stream = re.sub('\s*//.*\n', '\n', stream) # strip c++ style comments
    newdict = json.loads(stream)
    parseDict(newdict, path)
    return newdict
    #except:
    #    print "json load error:\n" + str(sys.exc_info()[1])
    #    return {}

# save the property tree starting at pynode into a json xml file.
def save(filename, node=root):
    try:
        f = open(filename, 'w')
        json.dump(node, f, indent=4, sort_keys=True)
        f.close()
    except:
        print filename + ": json save error:\n" + str(sys.exc_info()[1])
        return
