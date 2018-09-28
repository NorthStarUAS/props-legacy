#!/usr/bin/python3

from props import PropertyNode, root, getNode
import props_xml
import props_json
import sys

# run the system through it's paces

xmlfile = sys.argv[1]
jsonfile = sys.argv[2]

config = PropertyNode()
props_xml.load(xmlfile, config)
props_json.save(jsonfile, config)
