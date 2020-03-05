dnl Process this file with autogen.sh to produce a working configure
dnl script.

dnl Require at least automake 2.52
AC_PREREQ(2.52)

dnl Initialize the autoconf system (provide project name and version)
AC_INIT([pyprops], [1.1])

dnl Sanity check of the distribution
AC_CONFIG_SRCDIR([src/pyprops.h])

dnl Initialize the automake system
AM_INIT_AUTOMAKE

dnl Checks for programs.
AC_PROG_MAKE_SET
AC_PROG_CC
AC_PROG_CPP
AC_PROG_CXX
AC_PROG_RANLIB
AC_PROG_INSTALL
AC_PROG_LN_S

dnl echo "AR is $AR"
dnl if test -z "${AR+set}"; then
dnl   AR=ar
dnl fi
dnl echo "AR is $AR"
dnl AC_SUBST(AR)

dnl set the $host variable based on local machine/os
AC_CANONICAL_HOST

dnl check for default libraries
#AC_SEARCH_LIBS(clock_gettime, [rt])
#AC_SEARCH_LIBS(cos, [m])
#AC_SEARCH_LIBS(gzopen, [z])

# dnl find python primary
# AM_PATH_PYTHON([3])
# AC_PATH_PROGS([PYTHON_CONFIG],
#               [python$PYTHON_VERSION-config python-config],
#               [no],
#               [`dirname $PYTHON`])
# AS_IF([test "$PYTHON_CONFIG" = no], [AC_MSG_ERROR([cannot find python-config for $PYTHON.])])
# PYTHON_INCLUDES=`$PYTHON_CONFIG --includes`
# PYTHON_INCLUDES=""
# AC_MSG_RESULT([$PYTHON_INCLUDES])
# AC_SUBST(PYTHON_INCLUDES)
# PYTHON_LIBS=`$PYTHON_CONFIG --libs`
# PYTHON_LIBS="-lpython2.7"
# AC_MSG_RESULT([$PYTHON_LIBS])
# AC_SUBST(PYTHON_LIBS)

# To make the build more straight forward (hopefully) on cross compiled
# devel environments, hard code the libpython libraries
# you can use python3-config --includes --libs to find this info
PYTHON_INCLUDES="-I/usr/include/python3.7m"
PYTHON_LIBS="-lpython3.7m"
AC_SUBST(PYTHON_INCLUDES)
AC_SUBST(PYTHON_LIBS)

AM_CONFIG_HEADER(src/pyprops_config.h)

AC_CONFIG_FILES([ Makefile src/Makefile ])
AC_OUTPUT

