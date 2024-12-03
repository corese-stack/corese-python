#!/usr/bin/env python
# coding: utf-8
#
# Demonstrate loading and querying data with CoreseAPI
#


import getopt
import os
import sys

# import corese-python
sys.path.append(os.path.abspath(os.path.join(__file__,'..', '..','src')))
from  pycorese.api import CoreseAPI


# path to the RDF file
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'data',
                                         'beatles.rdf'))

usage = """simple_query.py [-b bridge] [-j file.jar]

-b bridge   | --bridge=bridge      choose beetwen py4j and (experimental) jpype bridge
-j file.jar | --javalib=file.jar   specify a jar file to bridge to

ex:
  simple_query.py -j /tmp/core-library.jar
  simple_query.py -b jpype
"""

# simple user interface
try:
    opts, args = getopt.getopt(sys.argv[1:],"b:j:",["bridge=", "javalib="])
except getopt.GetoptError:
    print(usage)
    sys.exit(-1)

# bridget selection
bridge = 'py4j'
javalib = None
for opt, arg in opts:
    if opt == '-b':
        bridge = arg
    if opt == '-j':
        javalib = arg

corese = CoreseAPI(java_bridge=bridge,
                   corese_path=javalib)
corese.loadCorese()

graph = corese.loadRDF(data_path)
print("Graph size: ", graph.graphSize())

#results = corese.sparqlSelect(graph)
#print(results)

sys.exit(0)

#
graph = corese.Graph()

# NameSpace
ex = "http://example.org/"

# Create and add statement: Edith Piaf is an Singer
edith_Piaf_IRI = graph.addResource(ex + "EdithPiaf")
rdf_Type_Property = graph.addProperty(corese.Namespaces.RDF + 'type')
singer_IRI = graph.addResource(ex + "Singer")

graph.addEdge(edith_Piaf_IRI, rdf_Type_Property, singer_IRI)

query = "select ?s ?p ?o where {?s ?p ?o}"

exec = corese.QueryProcess.create(graph)

results = exec.query(query)

print(results)
