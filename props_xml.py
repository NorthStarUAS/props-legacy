import os.path
import sys
import xml.etree.ElementTree as ET

from props import PropertyNode, root

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
            load(filename, pynode.__dict__[xmlnode.tag])
        else:
            # leaf
            pynode.__dict__[xmlnode.tag] = xmlnode.text
        
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
