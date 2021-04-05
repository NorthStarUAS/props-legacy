#!/usr/bin/python3

from distutils.core import setup

setup(name='props.py',
      version='1.2',
      description='Python Property Tree: flexible, robust shared program state between modules',
      author='Curtis L. Olson',
      author_email='curtolson@flightgear.org',
      url='https://github.com/RiceCreekUAS/rc-props',
      py_modules=['props', 'props_json', 'props_xml']
     )
