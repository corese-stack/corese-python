""" This module contains tests for the coreseAPI class."""


import os
import pytest
import sys

import pandas

from pycorese.api import CoreseAPI
import pycorese.corese_version as pv


class Test_py4j_run:
    """test p4yj queries"""

    # run only once
    @classmethod
    def setup_class(cls):
        #
        # global variable depending on the running context
        # (CI/github, local build)
        topdir = os.environ.get('GITHUB_WORKSPACE' ,
                                os.path.abspath(os.path.join(__file__,
                                                             '..',
                                                             '..')))

        cls.rdf_file = os.path.join( topdir,
                                     "python_examples",
                                     "data",
                                     "beatles.rdf")

        cls.ttl_file = os.path.join( topdir,
                                     "python_examples",
                                     "data",
                                     "beatles-validator.ttl")

        cls.corese_path = os.path.join(topdir,
                                       "build",
                                       "libs",
                                       f'corese-python-{pv.corese_version}-jar-with-dependencies.jar')


        # init localCorese (multiple localCorese may provoque errors_
        cls.corese = CoreseAPI( corese_path = cls.corese_path)
        cls.corese.loadCorese()
        print(cls.corese.engineVersion())


    # run before each test function
    def setUp(self):
        os.environ.pop('CORESE_PATH', None)


    def test_py4j_loadRDF(self):
        # to reduce the length of next lines of code
        corese = Test_py4j_run.corese

        # simple query
        query = 'SELECT * WHERE {?s ?p ?o} LIMIT 5'

        graph = corese.loadRDF(Test_py4j_run.rdf_file)
        results = corese.sparqlSelect(graph,
                                      query=query,
                                      return_dataframe=True)

        # result class
        assert(isinstance(results, pandas.core.frame.DataFrame))

        # number of elements
        assert(results.shape[0] == 5)

        # elements are triplets
        assert(results.shape[1] == 3)


    def test_py4j_inference(self):
        corese = Test_py4j_run.corese

        query = 'select * where {?s a ?type} order by ?type'

        graph = corese.loadRDF(Test_py4j_run.rdf_file)
        corese.resetRuleEngine(graph)

        #
        corese.sparqlSelect(graph, query=query)
        assert(graph.graphSize() == 29)

        #
        corese.loadRuleEngine(graph, profile=corese.RuleEngine.Profile.RDFS)
        assert(graph.graphSize() == 33)
