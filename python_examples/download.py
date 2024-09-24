#!/usr/bin/env python
#
# download necessary corese jar files
#

import getopt
import sys
from pathlib import Path

from maven_artifact.artifact import Artifact
from maven_artifact.downloader import Downloader
from maven_artifact.requestor import RequestException


def build_repo(artifact):
    """
    Get local maven repository from artifact name
    """

    maven_repository = Path.home().joinpath(".m2",
                                            "repository",
                                            artifact.path())
    maven_repository.mkdir(parents=True, exist_ok=True)

    filename = maven_repository.joinpath(artifact.artifact_id + "-" + artifact.version + "." + artifact.extension)

    print(f"filename={filename}")
    ######## expected "/Users/jls/.m2/repository/fr/inria/corese/corese-core/4.5.0/corese-core-4.5.0.jar"

    return filename


# global vars
package = "corese-core"
version = "4.5.0"

usage= f"""download.py [-v VER] [-p PKG]

download corese-core and corese-python from maven

-v VER  | --version==VER   specify a specific version (default={version})
-p PKG  | --package==PKG   specify a package name (default={package})

ex:
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

try:
    dl = Downloader(base="https://repo.maven.apache.org/maven2/", username=None, password=None, token=None)

    artifact = Artifact.parse("fr.inria.corese:"+package+":jar:"+version)
    filename = build_repo(artifact)

    if dl.download(artifact, filename, "md5"):
        sys.exit(0)
    else:
        print("Download failed.")
        sys.exit(1)
except RequestException as e:
    print(e.msg)
    sys.exit(1)
