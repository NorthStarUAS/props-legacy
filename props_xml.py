# TODO: properly handle enumerated nodes

import os.path
import sys
#import xml.etree.ElementTree as ET
import lxml.etree as ET

from props import PropertyNode, root

# internal xml tree parsing routine
def _parseXML(pynode, xmlnode, basepath):
    merge  = 'merge' in xmlnode.attrib
    exists = xmlnode.tag in pynode.__dict__
    if len(xmlnode) or 'include' in xmlnode.attrib:
        # has children
        newnode = PropertyNode()
        if 'include' in xmlnode.attrib:
            filename = basepath + '/' + xmlnode.attrib['include']
            print "calling load():", filename, xmlnode.attrib
            load(filename, newnode)
        if 'n' in xmlnode.attrib:
            # enumerated node
            n = int(xmlnode.attrib['n'])
            if not exists:
                pynode.__dict__[xmlnode.tag] = []
            elif not type(pynode.__dict__[xmlnode.tag]) is list:
                savenode = pynode.__dict__[xmlnode.tag]
                pynode.__dict__[xmlnode.tag] = [ savenode ]
            tmp = pynode.__dict__[xmlnode.tag]
            pynode.extendEnumeratedNode(tmp, n)
            pynode.__dict__[xmlnode.tag][n] = newnode
        elif exists:
            if not merge:
                # append
                print "node exists:", xmlnode.tag, "merge:", merge
                if not type(pynode.__dict__[xmlnode.tag]) is list:
                    # we need to convert this to an enumerated list
                    print "converting node to enumerate"
                    savenode = pynode.__dict__[xmlnode.tag]
                    pynode.__dict__[xmlnode.tag] = [ savenode ]
                pynode.__dict__[xmlnode.tag].append(newnode)
            else:
                # merge (follow existing tree)
                newnode = pynode.__dict__[xmlnode.tag]
        else:
            # create new node
            pynode.__dict__[xmlnode.tag] = newnode
        for child in xmlnode:
            _parseXML(newnode, child, basepath)
    else:
        # leaf
        if 'n' in xmlnode.attrib:
            # enumerated node
            n = int(xmlnode.attrib['n'])
            if not exists:
                pynode.__dict__[xmlnode.tag] = []
            elif not type(pynode.__dict__[xmlnode.tag]) is list:
                savenode = pynode.__dict__[xmlnode.tag]
                pynode.__dict__[xmlnode.tag] = [ savenode ]
            tmp = pynode.__dict__[xmlnode.tag]
            pynode.extendEnumeratedNode(tmp, n)
            pynode.__dict__[xmlnode.tag][n] = xmlnode.text
            print "leaf:", xmlnode.tag, xmlnode.text, xmlnode.attrib
        elif exists:
            if not merge:
                # append
                if not type(pynode.__dict__[xmlnode.tag]) is list:
                    # convert to enumerated.
                    print "converting node to enumerate"
                    savenode = pynode.__dict__[xmlnode.tag]
                    pynode.__dict__[xmlnode.tag] = [ savenode ]
                pynode.__dict__[xmlnode.tag].append(xmlnode.text)
            else:
                # overwrite
                pynode.__dict__[xmlnode.tag] = xmlnode.text
        elif type(xmlnode.tag) is str:
            pynode.__dict__[xmlnode.tag] = xmlnode.text
        else:
            print "Skipping unknown node:", xmlnode.tag, ":", xmlnode.text
                
# load xml file and create a property tree rooted at the given node
# supports <mytag include="relative_file_path.xml" />
def load(filename, pynode):
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

def _buildXML(xmlnode, pynode):
    for child in pynode.__dict__:
        node = pynode.__dict__[child]
        if isinstance(node, PropertyNode):
            xmlchild = ET.Element(child)
            xmlnode.append(xmlchild)
            _buildXML(xmlchild, node)
        elif type(node) is list:
            for i, ele in enumerate(node):
                if isinstance(ele, PropertyNode):
                    xmlchild = ET.Element(child)
                    xmlnode.append(xmlchild)
                    _buildXML(xmlchild, ele)
                else:
                    xmlchild = ET.Element(child)
                    xmlchild.text = str(ele)
                    xmlnode.append(xmlchild)
   
        elif type(child) is str:
            xmlchild = ET.Element(child)
            xmlchild.text = str(node)
            xmlnode.append(xmlchild)
        else:
            print "skipping:", child, ":", str(node)
        
# save the property tree starting at pynode into an xml file.
def save(filename, pynode=root):
    xmlroot = ET.Element('PropertyList')
    xml = ET.ElementTree(xmlroot)
    _buildXML(xmlroot, pynode)
    try:
        xml.write(filename, encoding="us-ascii", xml_declaration=False,
                  pretty_print=True)
    except:
        print filename + ": xml write error:\n" + str(sys.exc_info()[1])
        return