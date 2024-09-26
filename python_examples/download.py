#!/usr/bin/env python
#
# download corese jar files
#


import getopt
import os
import sys
#import pycorese.maven_tools as pmt

# import corese-python
sys.path.append(os.path.abspath(os.path.join(__file__,'..', '..','src')))
import pycorese.maven_tools as pmt

# global vars
package = "corese-core"
version = "4.5.0"

usage= f"""download.py [-v VER] [-p PKG]

download corese-core and corese-python from maven

-v VER  | --version==VER   specify a specific version (default={version})
-p PKG  | --package==PKG   specify a package name (default={package})

ex:
  download.py
  download.py -v 4.5.0
  download.py -v 4.5.0 -p corese-core
  download.py -v 4.4.1 -p corese-server
"""

try:
    opts, args = getopt.getopt(sys.argv[1:],"v:p:",["version=", "package="])
except getopt.GetoptError:
    print(usage)
    sys.exit(-1)

for opt, arg in opts:
    if opt == '-v':
        version = arg
    if opt == '-p':
        package = arg

pmt.maven_download(package, version)

sys.exit(1)
