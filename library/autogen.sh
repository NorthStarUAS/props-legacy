#!/bin/sh

# set the correct cross compiler.  This needs to be in the default path
# echo Default C compiler is \"${CC:="arm-angstrom-linux-gnueabi-gcc"}\"
# echo Default C++ compiler is \"${CXX:="arm-angstrom-linux-gnueabi-g++"}\"

# make automake happy
for i in AUTHORS ChangeLog COPYING NEWS README; do
  if [ ! -f $i ]; then
    echo "creating empty $i file"
    touch $i
  fi
done

echo "Running aclocal"
aclocal

echo "Running autoheader"
AH_RESULT="src/pyprops_config.h.in"
autoheader
if [ ! -e "$AH_RESULT" ]; then
    echo "ERROR: autoheader didn't create $AH_RESULT!"
    exit 1
fi    

echo "Running automake --add-missing"
automake --add-missing

echo "Running autoconf"
autoconf

if [ ! -e configure ]; then
    echo "ERROR: configure was not created!"
    exit 1
fi

echo ""
echo "======================================"

echo ""
echo "Now you can run:"
echo ""
echo "$ mkdir build; cd build"
echo "$ ../configure CFLAGS=\"-Wall -O3\" CXXFLAGS=\"-Wall -O3\""
echo "$ sudo make install"
