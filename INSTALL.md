# Quick install instructions

    $ cd python
    $ sudo python3 setup.py install

# To install C++ interface (required for rcUAS/rc-flight)

    $ cd library
    $ ./autogen.sh
    $ mkdir build
    $ cd build
    $ ../configure CFLAGS="-Wall -O3" CXXFLAGS="-Wall -O3"
    $ make
    $ sudo make install