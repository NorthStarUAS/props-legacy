# aura-props
A pure python "Preperty Tree" system for: convenient sharing of shared data between modules, organizing data, sharing 'state' between python and C modules.

## Background

Every non-trivial program needs a way to share data between modules.
Traditional data encapsulation involves hiding and protecting a
module's data so that other modules cannot directly touch it.  Instead
any interaction with the module is through the module's carefully
crafted API.  This is called "data encapsulation" and it is the
foundation of object oriented programing.

Constructing an application's code modules and data in a carefully
packaged way is a great idea.  It is a very robust way to structure
your applications and avoid a large class of bugs that arise out of
careless data sharing.  However, ideology has to survive the real
world.  There is a reason C++ classes have static (shared) members and
friend functions.  There is a reason C++ supports global variable
space.  Real world programming challenges are often messier than the
book examples.

There are times when it makes the most sense to share data globaly
within your application. It just does.  (Sometimes it still makes
sense to use a goto.)

Aura-props provides a way to create shared data space within your
application in a friendly and well structured way.  With aura-props as
the backbone of your application, you receive many additional nice
services and structures.

## The "Property Tree"

## Sharing data between modules

## Sharing data between mixed C++ and Python applications

## Script feature for C++

## Easy I/O for reading and writing configuration files

## Best practices