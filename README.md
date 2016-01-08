# aura-props
A pure python "Preperty Tree" system for: convenient sharing of shared data between modules, organizing data, sharing 'state' between python and C modules.

## Background

Every non-trivial program needs a way to share data between modules.
Traditional data encapsulation involves hiding and protecting a
module's data so that other modules cannot directly touch it.  Instead
any interaction with the module's data is through the module's
carefully crafted API.  This is called "data encapsulation" and it is
at the foundation of object oriented programing.

Constructing an application's code modules and data in a carefully
packaged way is a great idea.  It is a very robust way to structure
your applications and avoid a large class of bugs that arise out of
careless data sharing.  However, every ideology has to eventually
survive on it's own in the real world.  There is a reason C++ classes
have static (shared) members and friend functions.  There is a reason
C++ supports global variable space.  Real world programming challenges
are often messier than the book examples.

There are times when it makes the most sense to share data globaly
within your application. It just does.  (Sometimes it still makes
sense to use a goto.)

Aura-props provides a way to create shared data space within your
application in a friendly and well structured way.  With aura-props as
the backbone of your application, you receive many additional nice
services and structures.

## The "Property Tree"

The aura-props module enables an application to easily build a tree of
important data to be shared throughout the program.  There is a single
shared 'root' node that is automatically created when the props module
is imported.  From there an application can start filling in the tree
very quickly.  For example, consider a reader/writer example of a
simple autopilot that reads an external gps and uses that data to
navigate.

### The writer module

The gps driver module could include the following (python) code:

from props import getNode, root

gps = getNode("/sensors/gps", create=True)
(lat, lon, alt, speed, ground_track) = read_gps()
gps.lat = lat
gps.lon = lon
gps.alt = alt
gps.speed = speed
gps.ground_track = ground_track

With this simple bit of code we have constructed our property tree,
read the gps, and shared the values with the rest of our application.
Done!

The getNode() function will find the specified path in the property
tree and return that node to you.  If you specify create=True, then
getNode() will automatically create the node (and all the parents and
grandparents of that node) if they don't already exist.  So in one
line of code we have constructed the portion of the property tree that
this module needs.

A propertynode is really just an open ended python class, so we can
then assign values to any attributes we wish to create.

### The reader module

The navigation module needs the gps information from the property tree
and do something with it.  The code starts out very similar, but watch
what we can do:

from props import getNode, root

gps = getNode("/sensors/gps", create=True)
waypoint = getNode("/navigation/route/target", create=True)
ap = getNode("/autopilot/settings", create=True)

heading = great_circle_route([gps.lat, gps.lon], [waypoint.lat, waypoint.lon])
ap.target_heading = heading

Did you see what happened there?  We first grabbed the shared gps
node, but we also grabbed the shared target waypoint node, and we
grabbed the autopilot settings node.

We quickly computed the heading from our current location to our
target waypoint and we wrote that back into the autopilot
configuration node.

### Initialization order.

## Sharing data between modules

## Sharing data between mixed C++ and Python applications

## Script feature for C++

## Easy I/O for reading and writing configuration files

## Best practices

## A note on threaded applications