lib_LIBRARIES = libpyprops.a

include_HEADERS = \
        pymodule.h \
        pyprops.h \
        python_sys.h

libpyprops_a_SOURCES = \
        pymodule.cpp \
        pyprops.cpp \
        python_sys.cpp

AM_CPPFLAGS = $(PYTHON_INCLUDES)

noinst_PROGRAMS = props_test

props_test_SOURCES = props_test.cpp
props_test_LDADD = libpyprops.a $(PYTHON_LIBS)
