""" This module contains tests for the coreseAPI class."""


import pytest
from pycorese.api import CoreseAPI

class Test_api:
    """test user inputs"""

    #  test constructor
    def test_init_default_bridge(self):
        c = CoreseAPI()
        assert(c.java_bridge == "py4j")

    def test_init_py4j_bridge(self):
        c = CoreseAPI(java_bridge = "PY4J")
        assert(c.java_bridge == "py4j")

    def test_init_jpype_bridge(self):
        c = CoreseAPI(java_bridge = "jpype")
        assert(c.java_bridge == "jpype")

    def test_bad_bridge(self):
        with pytest.raises(ValueError):
            CoreseAPI(java_bridge="user_mistake")


    def test_bad_location_py4j(self):
        with pytest.raises(FileNotFoundError):
            c = CoreseAPI(corese_path="/this/file/does/not/exists")
            c.loadCorese() # this will crash


    def test_bad_location_jpype(self):
        with pytest.raises(FileNotFoundError):
            c = CoreseAPI(corese_path="/this/file/does/not/exists",
                          java_bridge="jpype")
            c.loadCorese() # this will crash
