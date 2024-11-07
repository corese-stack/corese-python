""" This module contains tests for the coreseAPI class."""


import os
import pytest
import sys

from pycorese.api import CoreseAPI
import pycorese.corese_version as pv

class Test_api:
    """test user inputs"""

    # package provided/built jar file
    # corese_path = os.path.join(os.path.abspath(os.path.join(__file__,'..', '..')),
    #                            "build",
    #                            "libs",
    #                            f'corese-python-{pv.corese_version}-jar-with-dependencies.jar')
    corese_path = os.path.abspath(os.path.join(__file__,
                                               '..',
                                               '..',
                                               "build",
                                               "libs",
                                               f'corese-python-{pv.corese_version}-jar-with-dependencies.jar'))


    # run before each test function
    def setUp(self):
        # remove CORESE_PATH, which has an effect on the loaded jar
        os.environ.pop('CORESE_PATH', None)



    #  test constructor
    def test_init_default_bridge(self):
        c = CoreseAPI()
        assert(c.java_bridge == "py4j")

    def test_init_py4j_bridge(self):
        c = CoreseAPI(java_bridge = "PY4J")
        assert(c.java_bridge == "py4j")

    def test_bad_bridge(self):
        with pytest.raises(ValueError):
            CoreseAPI(java_bridge="user_mistake")


    def test_bad_location_py4j(self):
        with pytest.raises(FileNotFoundError):
            c = CoreseAPI(corese_path="/this/file/does/not/exists")
            c.loadCorese() # this will crash

    def test_py4j_version_none(self):
        c = CoreseAPI()

        # version not found since corese is  not loaded
        assert(c.coreseVersion() is None)

    def test_py4j_version_default(self):

        # effectively load the corese-python jar file
        c = CoreseAPI(corese_path = Test_api.corese_path)
        c.loadCorese()

        assert(c.coreseVersion() == pv.corese_version)
