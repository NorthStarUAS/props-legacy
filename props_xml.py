# TODO: properly handle enumerated nodes

import os.path
import sys
#import xml.etree.ElementTree as ET
import lxml.etree as ET

from props import PropertyNode, root

# internal xml tree parsing routine
def _parseXML(pynode, xmlnode, basepath):
    if len(xmlnode):
        # has children
        newnode = PropertyNode()
        if xmlnode.tag in pynode.__dict__:
            # node exists
            print "node exists:", xmlnode.tag
            if type(pynode.__dict__[xmlnode.tag]) is list:
                # all is well
                pynode.__dict__[xmlnode.tag].append( newnode )
                print "all is well appending to list:", len(pynode.__dict__[xmlnode.tag])
            else:
                # we need to convert this to an enumerated list
                print "converting node to enumerate"
                savenode = pynode.__dict__[xmlnode.tag]
                pynode.__dict__[xmlnode.tag] = [ savenode, newnode ]
        else:
            # create new node
            pynode.__dict__[xmlnode.tag] = newnode
        for child in xmlnode:
            _parseXML(newnode, child, basepath)
    else:
        if 'include' in xmlnode.attrib:
            pynode.__dict__[xmlnode.tag] = PropertyNode()
            filename = basepath + '/' + xmlnode.attrib['include']
            load(filename, pynode.__dict__[xmlnode.tag])
        else:
            # leaf
            if type(xmlnode.tag) is str:
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
    root.pretty_print()

def _buildXML(xmlnode, pynode):
    for child in pynode.__dict__:
        node = pynode.__dict__[child]
        if isinstance(node, PropertyNode):
            xmlchild = ET.Element(child)
            xmlnode.append(xmlchild)
            _buildXML(xmlchild, node)
        elif type(node) is list:
            for i, ele in enumerate(node):
                xmlchild = ET.Element(child)
                xmlnode.append(xmlchild)
                _buildXML(xmlchild, ele)
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
