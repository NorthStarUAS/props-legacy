#!/usr/bin/python

from props import PropertyNode, root, getNode
import props_xml
import props_json

# run the system through it's paces

n1 = getNode("/a/b/c/d/e/f/g", create=True)
n1.var1 = 42
n1.var2 = 43
print getNode("/a/b/c/d/e1/f/g", create=True)
n2 = getNode("/a/b/c/d/e/f/g", create=False)
print n2.__dict__
print getNode("a/b/c/d/e/f/g")

a = getNode("/a", create=False)
print "a dict=", a.__dict__
print a.b.c.d.e.f.g.var1

n3 = getNode("/a/b/c/d/e/f/g/var1", create=False)
print "n3:", n3
n3 = getNode("/a/b/c/d/e/f/g/var1", create=True)
print "n3:", n3

n4 = getNode("/a/b/c")
n5 = n4.getChild("d/e/f/g")
print n5.__dict__
n6 = n5.getChild("var1")
print n6

# correct way to create a path with a new child node
gps = getNode("/sensors/gps[5]", create=True)
gps.alt_m = 275.3

sensors = getNode("/sensors")
print "gps len = ", sensors.getLen("gps");

# az get's created a parent node
imu = getNode("/sensors/imu[2]", create=True)
# this works, but is bad form because az is originally created as a
# PropertyNode() branch that can't have a value, only childredn
imu.az = -9.80
# this should work
root.sensors.imu[2].az = -9.81

root.pretty_print()

print "alt_m:", root.sensors.gps[5].alt_m

config = getNode('/', create=True)
#file = '/home/curt/Source/AuraUAS/aura-data/config/main-skywalker.xml'
#props_xml.load(file, config)
#props_xml.save("testing.xml", config)
#props_json.save("testing.json", config)
newroot = PropertyNode()
props_json.load("/home/curt/Source/AuraUAS/aura-data/config/main-skywalker.json", newroot)
print "pretty:"
newroot.pretty_print()
quit()

print "sensor children:", sensors.getChildren()
for child in sensors.getChildren():
    node = sensors.getChild(child)
    print node

global_tasks = getNode("/config/mission/global_tasks");
print "global_tasks children:", global_tasks.getChildren()
print global_tasks.task[0].name

a = getNode("/task/home", True)
b = getNode("/task/home", True)
b.val = 123

c = getNode("/task", True)
print "leaf /task/home:", c.isLeaf("home")
print "leaf /task/home/val:", b.isLeaf("val")

d = getNode("/sensors/device", True)

d1 = getNode("/sensors/device[0]", True)
d1.var1 = "It is me!"

print "d:", d.getChildren()
print "d1:", d.getChildren()

getNode("/sensors").pretty_print()


air = getNode("/sensors/airdata", True)
air1 = sensors.getChild("/airdata[0]", True)
sensors.pretty_print()

b = getNode("/sensors/", True)
b.setLen("newattr", 10, 0.0)
print b.newattr
