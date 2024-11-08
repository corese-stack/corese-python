""" This module contains tests for the coreseAPI class."""


import os
import pytest
import sys

from pycorese.api import CoreseAPI
import pycorese.corese_version as pv

class Test_py4j_api:
    """test user inputs"""

    # run before each test function
    def setUp(self):
        # remove CORESE_PATH, which has an effect on the loaded jar
        os.environ.pop('CORESE_PATH', None)


    #  test constructor
    def test_init_default_bridge(self):
        corese = CoreseAPI()
        assert(corese.java_bridge == "py4j")

    def test_init_py4j_bridge(self):
        corese = CoreseAPI(java_bridge = "PY4J")
        assert(corese.java_bridge == "py4j")

    def test_bad_bridge(self):
        with pytest.raises(ValueError):
            CoreseAPI(java_bridge="user_mistake")


    def test_bad_location_py4j(self):
        with pytest.raises(FileNotFoundError):
            corese = CoreseAPI(corese_path="/this/file/does/not/exists")
            corese.loadCorese() # this will crash

    def test_py4j_version_none(self):
        corese = CoreseAPI()

        # version not found since corese is  not loaded
        assert(corese.engineVersion() is None)
