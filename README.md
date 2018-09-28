# aura-props

Aura-props is a pure python "property tree" system for convenient
organization and sharing of data between code modules.

Aura-core (available separately) includes a C++ interface so that the
property tree can also serve as a simple mechanism for sharing data
between mixed python/C++ modules (without needing to run the gauntlet
of the very tricky python API.)

Traditionally code modules pass data through a rigid (and often
brittle or clunky) API defined by each module.  The property tree
establishes an organized tree of data that is shared and accessible by
all modules in the application.  It assumes some basic cooperation and
rule following between modules, but there are many very nice outcomes
to this approach.

## Quick Installation Guide

Please notice there is two parts to the install process (the python
install and the C library install)

### Part 1

    $ cd python
    $ sudo python3 ./setup.py install

### Part 2

    $ cd ../library
    $ ./autogen.sh
    $ mkdir build
    $ cd build
    $ ../configure CFLAGS="-Wall -O3" CXXFLAGS="-Wall -O3"
    $ make
    $ sudo make install


## Background

Every non-trivial program needs a way to share data between modules.
Traditional data encapsulation involves hiding and protecting a
module's data so that other modules cannot directly touch it.  Instead
any interaction with the module's data is through the module's
carefully crafted API.  This is called "data encapsulation" and it is
at the foundation of object oriented programming.

Constructing an application's modules and data in a carefully packaged
way is a great idea.  It is a very robust way to structure your
applications and avoid a large class of bugs that arise out of
careless data sharing.  However, every ideology has to eventually
survive on it's own in the real world.  There is a reason C++ classes
have static (shared) members and friend functions.  There is a reason
C++ supports global variable space.  Real world programming challenges
are often messier than the book examples.

There are times when it makes the most sense to share data globally
within your application. It just does.  (Sometimes it still makes
sense to use a goto.)

Aura-props provides a way to create shared data space within your
application in a friendly and well structured way.  With aura-props as
the backbone of your application, you receive many additional nice
services and structures.

The original idea for the 'Property System' probably dates back to
long ago, but the first implementation that I am aware of grew up
within the FlightGear ecosystem.  It has proved to be so convenient
and nice that I have used it in several other large projects.

Now, here, I have re-imagined the property system, stripped down to
it's essentials, simplified, and rewritten entirely in python.

## The Property System

The word "System" is carefully chosen.  The Property System is an
interwoven network of concepts that can bring huge value to your
application.  It may not be the right choice for every application,
but in the right context it is super awesome.

* It provides structured data sharing between modules within your
  application.  (I.e. when your app needs global data shared, don't
  hack it and hide it, embrace it with a real structure that avoids
  the bad side of global variables.)
  
* It provides a way to organize the important data structures within
  your application (the property tree.)

* The new python implementation now enables rich data sharing between
  C++ and Python without forcing the C++ coder to wade through an
  obtuse Python C++ API.

* The property tree maps well to xml files enabling sophisticated
  configuration file support with a few easy function calls.

* The property tree can be exposed to external interfaces (i.e. via a
  network socket) to enable allowed external programs to conveniently
  access and even change items in the property tree.  This can be
  useful for debugging or for simple (low bandwidth) interaction
  between separate applications.

## The Property Tree

The aura-props module enables an application to easily build a tree of
important data to be shared throughout the program.  There is a single
shared 'root' node that is automatically created when the props module
is imported.  From there an application can start filling in the tree
very quickly.  For example, consider a reader/writer example of a
simple autopilot that reads an external gps and uses that data to
navigate.

A hierarchical tree structure is easy to understand, easy to organize,
easy to use, and keeps like data near each other.

### Example: writer module

The gps driver module could include the following (python) code:

```
from props import getNode, root
gps = getNode("/sensors/gps", create=True)
(lat, lon, alt, speed, ground_track) = read_gps()
gps.lat = lat
gps.lon = lon
gps.alt = alt
gps.speed = speed
gps.ground_track = ground_track
```

With this simple bit of code we have constructed our property tree,
read the gps, and shared the values with the rest of our application.
Done!

The getNode() function will find the specified path in the property
tree and return that node to you.  If you specify create=True, then
getNode() will automatically create the node (and all the parents and
grandparents of that node) if they don't already exist.  So in one
line of code we have constructed the portion of the property tree that
this module needs.

A pyPropertyNode is really just an open ended python class, so we can
then assign values to any attributes we wish to create.

### Example: reader module

The navigation module needs the gps information from the property tree
and do something with it.  The code starts out very similar, but watch
what we can do:

```
from props import getNode, root
gps = getNode("/sensors/gps", create=True)
waypoint = getNode("/navigation/route/target", create=True)
ap = getNode("/autopilot/settings", create=True)
heading = great_circle_route([gps.lat, gps.lon], [waypoint.lat, waypoint.lon])
ap.target_heading = heading
```

Did you see what happened there?  We first grabbed the shared gps
node, but we also grabbed the shared target waypoint node, and we
grabbed the autopilot settings node.  We quickly computed the heading
from our current location to our target waypoint and we wrote that
back into the autopilot configuration node.

This approach to sharing data between program modules is a bit unique.
But consider the alternatives: many applications grow their
inter-module communication ad-hoc as the code evolves and some of the
interfaces can become inconsistent or awkward as real world data gets
incrementally shoved into existing C++ class api's.  The result of the
ideological approach is often messy and clunky.

The property system provides an alternative for intra-application data
sharing that is simple, easy to understand, and just works.  It is a
different philosophy of programming from what many people are used to,
but the benefits and convenience of the property system quickly
becomes a way of life.

### Module initialization order.

Please notice that both the reader and writer modules in the above
example call getNode() with the create flag set to true.  The property
tree system allows initialization order independence among modules.
With respect to the property tree (ignoring other higher level
application specific dependencies) the modules can be initialized in
any order.  The first module to initialize and request the specific
property nodes will trigger their creation, and subsequent modules
will find the nodes already there.

### Direct access to properties (Python)

The property tree is constructed out of a thin python shell class.
Once the appropriate portions of the property tree are created and
populated, python code can directly reference nodes and values.  For
example, the following reference should work if the gps sensor tree
has been created and populated:

```
lat = props.sensors.gps.lat
```

### Sharing data between mixed C++ and Python applications

A C++ interface to the python property tree is being developed in
parallel.  For now, know that it exists and brings to C++ most of the
benefits of the property tree.  (And also enables data sharing between
applications that are a mix of C++ and Python.)

### Script features for C++

For the C++ developer: incorporating the Property Tree into your
application brings several conveniences of scripting languages to your
application.  One big convenience is automatic type conversion.  For
example, an application can write a string value into a field of the
property tree, but read it back out as a double.  Watch carefully:

```
#include "pyprops.hxx"
int main(int argc, char **argv) {
    // cleanup the python interpreter after all the main() and global
    // destructors are called
    atexit(pyPropsCleanup);
    
    pyPropsInit(argc, argv);

    pyPropertyNode gps_node = pyGetNode("/sensors/gps");

    gps_node.setString("lat", "-45.235");
    double lat = gps_node.getDouble("lat");

    return 0;
}
```

Did you see how the value of "lat" is written as a string constant,
but can be read back out as a double?  Often it is easy to keep your
types consistent, but it's nice to just let the back end system convert
types for you as needed.
 
### Performance considerations

Convenience comes at a cost.  The property tree has been designed in a
way to leverage existing native python structures so it is relatively
thin and fast, but within python scripts, saving a variable as a class
member does have more overhead that a standalone variable.  Within
C++, accessing property nodes and values requires a call layer into
python structures.  Thus reading and writing properties does involve
some additional overhead compared to using native variables.

The best recommendation is to place all calls to `getNode()` within a
modules initialization routine, cache the pointer that is returned,
and then use this pointer exclusively in the module's update routines.

This way the expensive getNode() function is only called during
initialization, and the faster class.field notation (Python) or get()
set() routines (C++) are called during run-time.

### Easy I/O for reading and writing configuration files

The hierarchical structure of the property tree maps nicely to xml and
json.  Currently there is an xml reader that loads an xml file and
populates populates the values into a newly created property (sub)
tree rooted at the requested location in the larger property tree.
This is a great way to load a big application config file with a
single function call.  Then the config values are available in the
property tree for the various modules to use as needed.

### A note on threaded applications

The Property Tree system is *not* thread safe.  I am pondering some
ideas to make a thread safe version of the property tree, but this
will add restrictions to the api and overhead for resource locking.
Hopefully I will add more on this later.

For now, if you include threads in your application, know that either
the property tree should be confined exclusively to one thread, or you
will need to take extra precautions within your own application to
ensure two threads do not try to read or write the property tree
simultaneously.  Doing so could lead to random and difficult to debug
program crashes.
