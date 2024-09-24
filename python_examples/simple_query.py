#!/usr/bin/env python
# coding: utf-8
#
# Demonstrate loading and querying data with CoreseAPI
#


import getopt
import os
import sys


# path to the RDF file
data_path = os.path.abspath(os.path.join('data', 'beatles.rdf'))

usage = """simple_query.py [-b bridge]

-b bridge | --bridge=bridge   choose beetwen py4j and (experimental) jpype bridge
"""

# simple user interface
try:
    opts, args = getopt.getopt(sys.argv[1:],"b:",["bridge="])
except getopt.GetoptError:
    print(usage)
    sys.exit(-1)

# bridget selection
bridge = 'py4j'
for opt, arg in opts:
    if opt == '-b':
        bridge = arg

# import corese-python
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from  pycorese.api import CoreseAPI

corese = CoreseAPI(java_bridge=bridge)
corese.loadCorese()

graph = corese.loadRDF(data_path)
results = corese.sparqlSelect(graph)

print(results)

sys.exit(0)

#
graph = corese.Graph()

# NameSpace
ex = "http://example.org/"

# Create and add statement: Edith Piaf is an Singer
edith_Piaf_IRI = graph.addResource(ex + "EdithPiaf")
rdf_Type_Property = graph.addProperty(corese.RDF.TYPE)
singer_IRI = graph.addResource(ex + "Singer")

graph.addEdge(edith_Piaf_IRI, rdf_Type_Property, singer_IRI)

query = "select ?s ?p ?o where {?s ?p ?o}"

exec = corese.QueryProcess.create(graph)

results = exec.query(query)

print(results)
