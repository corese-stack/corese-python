"""
Maven helpers to easy package downloads
"""


import logging
import sys
from pathlib import Path

from maven_artifact.artifact import Artifact
from maven_artifact.downloader import Downloader
from maven_artifact.requestor import RequestException


def artifact2filename(artifact,
                      makedir: bool = False):
    """
    Get local maven expected filename from artifact name
    """

    maven_repository = Path.home().joinpath(".m2",
                                            "repository",
                                            artifact.path())
    if makedir:
        maven_repository.mkdir(parents=True, exist_ok=True)

    filename = maven_repository.joinpath(artifact.artifact_id + "-" + artifact.version + "." + artifact.extension)

    #print(f"filename1={filename}")

    return filename


def package2filename(package: str,
                     version: str,
                     makedir: bool = False):
    """
    Build local maven expected filename from
    package name and version
    """

    jar = package + "-" + version + ".jar"
    maven_repository = Path.home().joinpath(".m2",
                                            "repository",
                                            "fr",
                                            "inria",
                                            "corese",
                                            package,
                                            version
                                            )

    if makedir:
        maven_repository.mkdir(parents=True, exist_ok=True)

    filename = maven_repository.joinpath(jar)

    print(f"filename={filename}")

    return filename


def maven_download(package: str = 'corese-core',
                   version: str = '4.5.0'):

    """
    given a corese package name and version,
    download/update it using maven
    """


    dl = Downloader(base="https://repo.maven.apache.org/maven2/",
                    username=None,
                    password=None,
                    token=None)


    artifact = Artifact.parse("fr.inria.corese:"+package+":jar:"+version)
    filename = package2filename(package = package,
                                version = version,
                                makedir = True)

    jar = package + "-" + version + ".jar"
    try:
        if dl.download(artifact, filename):
            logging.info(f"jar {jar} downloaded")
            return True
        else:
            print(f"download of {jar} failed.")
            return False
    except RequestException as e:
        print(e.msg)
