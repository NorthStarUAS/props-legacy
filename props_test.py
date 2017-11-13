#!/usr/bin/python

from props import root, getNode, getChild, getLen, pretty_print, getChildren, setRoot, isLeaf, setLen
import props_json

# run the system through it's paces

n1 = getNode("/a/b/c/d/e/f/g", create=True)
n1['var1'] = 42
n1['var2'] = 43
print getNode("/a/b/c/d/e1/f/g", create=True)
n2 = getNode("/a/b/c/d/e/f/g", create=False)
print 'n2:', n2
print getNode("a/b/c/d/e/f/g")  # fail, no leading slash
print n2['var1']

a = getNode("/a", create=False)
print "a", a

n3 = getNode("/a/b/c/d/e/f/g/var1", create=False) # fail, is a leaf node
print "n3:", n3
n3 = getNode("/a/b/c/d/e/f/g/var1", create=True) # fail, already defined as leaf node
print "n3:", n3

n4 = getNode("/a/b/c")
n5 = getChild(n4, "d/e/f/g")
print 'n5:', n5
n6 = getChild(n5, "var1")
print 'n6:', n6

# correct way to create a path with a new child node
gps = getNode("/sensors/gps[5]", create=True)
gps['alt_m'] = 275.3

sensors = getNode("/sensors")
print 'sensors:', sensors
print "gps len =", getLen(sensors, 'gps')
print 'n5/var1 len =', getLen(n5, 'var1') # fail, not enumerated
print 'n5/var3 len =', getLen(n5, 'var3') # fail, doesn't exist

# az get's created a parent node
imu = getNode("/sensors/imu[2]", create=True)
# this works, but is bad form because az is originally created as a
# PropertyNode() branch that can't have a value, only childredn
imu['az'] = -9.80

pretty_print(root)

print "alt_m:", sensors['gps'][5]['alt_m']

config = props_json.load("/home/curt/Projects/AuraUAS/aura-config/config/main-skywalker.json")
print "pretty:"
pretty_print(config)

props_json.save('test.json', config)

setRoot(config)
print 'pretty2:'
pretty_print(root)
sensors = getNode("/config/sensors")
print "sensor children:", getChildren(sensors)
for child in getChildren(sensors):
    node = getChild(sensors, child)
    print node

global_tasks = getNode("/config/mission/global_tasks");
print "global_tasks children:", getChildren(global_tasks)
print global_tasks['task'][0]['name']

a = getNode("/task/home", True)
b = getNode("/task/home", True)
b['val'] = 123

c = getNode("/task", True)
print "leaf /task/home:", isLeaf(c, "home")
print "leaf /task/home/val:", isLeaf(b, "val")

d = getNode("/sensors/device", True)

d1 = getNode("/sensors/device[0]", True)
d1['var1'] = "It is me!"

print "d:", getChildren(d)
print "d1:", getChildren(d1)

pretty_print(getNode("/sensors"))


air = getNode("/sensors/airdata", True)
air1 = getChild(sensors, "/airdata[0]", True)
pretty_print(sensors)

b = getNode("/sensors/", True)  # generates a sloppy coder warning
setLen(b, "newattr", 10, 0.0)
print b['newattr']
