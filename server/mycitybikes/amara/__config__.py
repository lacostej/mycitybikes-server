# Configuration variables
NAME     = 'Amara'
VERSION  = '1.2a2'
FULLNAME = 'Amara-1.2a2'
URL      = 'http://uche.ogbuji.net/tech/4suite/amara/'

import sys
if getattr(sys, 'frozen', False):
    # "bundled" installation locations (e.g., py2exe, cx_Freeze)
    RESOURCEBUNDLE = True
    PYTHONLIBDIR   = '/'
    BINDIR         = None
    DATADIR        = '/Share'
    SYSCONFDIR     = None
    LOCALSTATEDIR  = None
    LIBDIR         = None
    LOCALEDIR      = '/Share/Locale'
else:
    # standard distutils installation directories
    RESOURCEBUNDLE = False
    PYTHONLIBDIR   = '/usr/lib/python2.5/site-packages/'
    BINDIR         = '/usr/bin'
    DATADIR        = '/usr/share/Amara'
    SYSCONFDIR     = '/usr/etc/Amara'
    LOCALSTATEDIR  = '/usr/var/Amara'
    LIBDIR         = '/usr/lib/Amara'
    LOCALEDIR      = '/usr/share/locale'
del sys
