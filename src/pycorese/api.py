import pandas as pd
from io import StringIO
import os
import re
from collections import namedtuple
from typing import Optional

def _isFile(input: str):
    file_path_pattern = r'^(?:[a-zA-Z]:\\|\.{1,2}[\\\/]|\/)?(?:[\w\-\s]+[\\\/]?)+[\w\-\s]+\.[\w]+$'

    if re.match(file_path_pattern, input):
        if os.path.isfile(input):
            return True
        else:
            raise FileNotFoundError (f"The file {input} does not exist.")

    return False

def _is_url(input: str):
    url_pattern = r'^https?://.*\.[\w]+$'
    return re.match(url_pattern, input) is not None

def _is_rdf_xml(content):
    rdf_xml_pattern = r'^\s*<\?xml.*\?>.*<rdf:RDF'
    return re.search(rdf_xml_pattern, content, re.DOTALL) is not None

def _is_turtle(content):
    turtle_pattern = r'(@prefix|@base|<[^>]+>\s*<[^>]+>\s*<[^>]+>|<[^>]+>\s*<[^>]+>\s*"[^"]*")'
    return re.search(turtle_pattern, content) is not None


class CoreseAPI:
    """
    Simplified API to leverage functionality of Corese Java library ``corese-core``.

    Parameters
    ----------
    java_bridge : str, optional
        Package name to use for Java integration. Options: ``py4j``, ``jpyp``. Default is ``py4j``.
    corese_path : str, optional
        Path to the corese-python library. If not specified (default), the jar
        file that was installed with the package is used.
    """

    def __init__(self,
                 java_bridge: str = 'py4j',
                 corese_path: Optional[str] = None):

        if java_bridge.lower() not in ['py4j', 'jpype']:
            raise ValueError('Invalid java bridge. Only "py4j" and "jpype" are supported.')

        self.corese_path = corese_path
        self.java_bridge = java_bridge.lower()
        self.java_gateway = None
        self._bridge = None

        # This is a minimum set of Corese classes required for the API to work
        self.Graph = None        # Corese ``fr.inria.corese.core.Graph`` object
        self.QueryProcess = None # Corese ``fr.inria.corese.core.query.QueryProcess`` object
        self.ResultFormat = None # Corese ``fr.inria.corese.core.print.ResultFormat`` object
        self.Load = None         # Corese ``fr.inria.corese.core.load.Load`` object
        self.RuleEngine = None   # Corese ``fr.inria.corese.core.rule.RuleEngine`` object
        self.Transformer = None  # Corese ``fr.inria.corese.core.transform.Transformer`` object
        self.Shacl = None        # Corese ``fr.inria.corese.core.shacl.Shacl`` object
        self._DataManager = None  # Corese ``fr.inria.corese.core.storage.api.dataManager.DataManager`` object
        self._CoreseGraphDataManager = None # Corese ``fr.inria.corese.core.storage.CoreseGraphDataManager`` object
        self._CoreseGraphDataManagerBuilder = None # Corese ``fr.inria.corese.core.storage.CoreseGraphDataManagerBuilder`` object


    def coreseVersion(self)-> str|None:
        """
        Get the version of the corese-core library.

        Notes
        -----
        Corese library  must be loaded first.

        Returns
        -------
        str
            The version of the   ``corese-core``   library used. If the library is not loaded, returns None.
        """

        #TODO: implement this to call the coreseVersion() from
        # the corese engine (at the moment this method is static and
        # may return bad result)

        if self._bridge is None:
            print("Corese engine is not loaded yet")
            return None

        return self._bridge.coreseVersion()

    def loadCorese(self) -> Optional[object]:
        """
        Load Corese library into JVM and expose the Corese classes.

        Returns
        -------
        object
            Java Gateway object if the library is loaded successfully. Otherwise, returns None.
        """
        #TODO: refactor
        if self.java_bridge == 'py4j':

            from .py4J_bridge import Py4JBridge

            self._bridge = Py4JBridge(corese_path = self.corese_path)
            self.java_gateway = self._bridge.loadCorese()
        else:

            from .jpype_bridge import JPypeBridge

            self._bridge = JPypeBridge(corese_path = self.corese_path)
            self.java_gateway =self._bridge.loadCorese()

        # This is a minimum set of classes required for the API to work
        # if we need more classes we should think about how to expose
        # them without listing every single one of them here
        self.Graph = self._bridge.Graph
        self.Load = self._bridge.Load
        self.Loader = self._bridge.Loader
        self.QueryProcess = self._bridge.QueryProcess
        self.ResultFormat = self._bridge.ResultFormat
        self.RuleEngine = self._bridge.RuleEngine
        self.Transformer = self._bridge.Transformer

        # Classes to manage Graph(s) with different storage options
        self._DataManager = self._bridge.DataManager
        self._CoreseGraphDataManager = self._bridge.CoreseGraphDataManager
        self._CoreseGraphDataManagerBuilder = self._bridge.CoreseGraphDataManagerBuilder

        # Classes to manage SHACL validation
        self.Shacl  = self._bridge.Shacl

        # Define the known namespaces
        Namespace = namedtuple('Namespace', ['RDF', 'RDFS', 'SHACL'])
        self.Namespaces = Namespace(
            self._bridge.RDF.RDF,
            self._bridge.RDFS.RDFS,
            'http://www.w3.org/ns/shacl#'
        )

        self.SHACL_REPORT_QUERY=f'''@prefix sh: <{self.Namespaces.SHACL}> .
                                   SELECT ?o ?p ?s
                                   WHERE {{ ?o a sh:ValidationResult.
                                            ?o ?p ?s.}}'''

        return self.java_gateway

    def unloadCorese(self):
        """
        Explicitly unload Corese library.

        It's not necessary to call this method, as the library is automatically
        unloaded when the Python interpreter exits.

        Warning
        -------
        After unloading Corese bridged by ``JPype`` it is not possible to restart it.
        """
        self._bridge.unloadCorese()

        self.java_gateway = None

        self.Graph = None
        self.QueryProcess = None
        self.ResultFormat = None
        self.Load = None

    #TODO: Add support for the other RDF formats
    def loadRDF(self, rdf: str, graph: Optional[object] = None)-> object:
        """
        Load RDF file/string into Corese graph. Supported formats are RDF/XML and Turtle.

        Parameters
        ----------
        rdf : str
            Path or URL of an RDF file or a string with RDF content.
        graph : object, optional
            Corese ``fr.inria.corese.core.Graph`` object.
            If an object is not provided (default), new Graph and GraphManager will be created.

        Returns
        -------
        object
            Corese ``fr.inria.core.Graph`` object.
        """
        if not self.java_gateway:
            self.loadCorese()

        assert self.Graph, 'Corese classes are not loaded properly.'
        assert self.Load, 'Corese classes are not loaded properly.'

        #TODO: add support for DataManager(s) for different storage options
        # the option has to come as a parameter
        # if not graph:
        #     graph = self.Graph()
        #     graph_mgr = self.CoreseGraphDataManagerBuilder().build()
        # else:
        #     graph_mgr = self.CoreseGraphDataManagerBuilder().graph(graph).build()
        #
        # ld = self.Load.create(graph, graph_mgr)
        # ...
        # return graph_mgr.getGraph()

        graph = graph or self.Graph()

        ld = self.Load.create(graph)

        #TODO: add support for a URL
        if _isFile(rdf):
            ld.parse(rdf)
        elif _is_url(rdf):
            ld.parse(rdf)
        else:
            if _is_rdf_xml(rdf):
                ld.loadString(rdf, self.Loader.format.RDFXML_FORMAT)
            elif _is_turtle(rdf):
                ld.loadString(rdf, self.Loader.format.TURTLE_FORMAT)
            else:
                raise ValueError('Unsupported RDF format. Only RDF/XML and Turtle are supported by this version')

        return graph.getGraph()

    def loadRuleEngine(self, graph: object,
                             profile: str,
                             replace:bool = False)-> object:
        """
        Load the rule engine for a given graph.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        profile : str
            Profile the rule engine. Accepted values: Accepted values: *rdfs*, *owlrl*, *owlrl_lite*, *owlrl_ext*
        replace : bool, optional
            Replace the existing rule engine. Default is False.

        Returns
        -------
        object
            Corese ``fr.inria.core.rule.RuleEngine`` object.
        """
        assert self.RuleEngine, 'Corese classes are not loaded properly.'
        assert graph, 'Graph object is required.'
        assert profile, 'Profile object is required.'

        if profile == 'rdfs':
            profile = self.RuleEngine.Profile.RDFS
        elif profile == 'owlrl_lite':
            profile = self.RuleEngine.Profile.OWLRL_LITE
        elif profile == 'owlrl_ext':
            profile = self.RuleEngine.Profile.OWLRL_EXT
        elif profile == 'owlrl':
            profile = self.RuleEngine.Profile.OWLRL
        else:
            raise ValueError('Invalid profile. Accepted values are: "rdfs", "owlrl_lite", "owlrl_ext", "owlrl"')

        if replace:
            self.resetRuleEngine(graph)

        rule_engine = self.RuleEngine.create(graph)

        rule_engine.setProfile(profile)
        rule_engine.process()

        return rule_engine

    def resetRuleEngine(self, graph: object)-> None:
        """
        Reset the rule engine for a given graph.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        """
        assert self.RuleEngine, 'Corese classes are not loaded properly.'
        assert graph, 'Graph object is required.'

        rule_engine = self.RuleEngine.create(graph.getGraph())
        rule_engine.remove()

    def parsePrefixes(self, query: str)-> dict:
        """
        Parse a query string to extract a dictionary of (prefix, namespace) pairs

        Parameters
        ----------
        query : str
            Query string that may contain PREFIX declarations

        Returns
        -------
        dict
            Dictionary of (prefix, namespace) pairs or an empty dictionary if no prefixes are found.
        """
        pattern = re.compile(r'PREFIX\s+(\w+):\s+<\s*(.*?)\s*>')
        matches = pattern.findall(query)
        prefixes = {prefix + ':' : url for prefix, url in matches}
        return prefixes

    def _applyPrefixes(self, query_result: object|pd.DataFrame, ns: dict|None)-> object|pd.DataFrame:
        """
        Substitute long namespace names in the URIs with  prefixes. This method can be applied either
        to a Corese query result map or a DataFrame.

        applying prefixes to a DataFrame is faster since it is done in python. Applying prefixes to a map
        is slower since it is done in the Java process for each value.

        Parameters
        ----------
        query_result : object or pd.DataFrame
            Query result in Corese format or a DataFrame.
        ns : dict, optional
            Dictionary of (prefix, namespace) pairs. Default is None.

        Returns
        -------
        object or pd.DataFrame
            Query result with prefixes applied.
        """

        if not isinstance(ns, dict):
            return query_result

        if isinstance(query_result, pd.DataFrame):
            # prefix in the DataFrame -fast
            return query_result.fillna('')\
                    .replace(ns.values(), ns.keys(), regex=True)\
                    .replace('',pd.NA,regex = True)
        else:
            # assume it's a map output of the query -slow
            for i, row in enumerate(query_result.getMappingList()):
                for j, var in enumerate(row.getList()):
                    if not var.isEmpty() and var.size() > 1 and var[1].isURI():
                        for prefix, namespace in ns.items():
                            if var[1].contains(namespace):
                                new_uri = var[1].stringValue().replace(namespace, prefix)
                                var[1].setValue(new_uri)

            return query_result

    def sparqlSelect(self, graph: object,
                    query: str ='SELECT * WHERE {?s ?p ?o} LIMIT 5',
                    return_dataframe: bool =True,
                    post_apply_prefixes: bool = True)-> object|pd.DataFrame:
        """
        Execute SPARQL SELECT or ASK query on Corese graph. Optionally return the result as DataFrame.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        query : str, optional
            SPARQL query. By default five first triples of the graph are returned.
        return_dataframe : bool, optional
            Return the result as a DataFrame. Default is True.
        post_apply_prefixes : bool, optional
            Substitute long namespaces with prefixes defined in the query . Default is True.

        Returns
        -------
        object or pd.DataFrame
            Result of the SPARQL query in CSV-formatted  ``fr.inria.core.print.ResultFormat``
            object or a ``pandas.DataFrame``.
        """
        assert self.QueryProcess, 'Corese classes are not loaded properly.'
        assert self.ResultFormat, 'Corese classes are not loaded properly.'

        if not graph:
            raise ValueError('Graph object is required.')

        # create a dictionary of (prefix, namespace) pairs
        ns = self.parsePrefixes(query)

        exec = self.QueryProcess.create(graph)
        map = exec.query(query)

        # to keep it simple for now return the result in CSV format
        result = self.ResultFormat.create(map, self.ResultFormat.SPARQL_RESULTS_CSV)

        # or return a DataFrame
        if return_dataframe:
            if post_apply_prefixes:
                return self._applyPrefixes(self.toDataFrame(result), ns)
            else:
                return self.toDataFrame(result)

        return result

    def toDataFrame(self, queryResult: object,
                            dtypes: list|dict|None = None)-> pd.DataFrame:
        """
        Convert Corese ResultFormat object to ``pandas.DataFrame``.

        Parameters
        ----------
        queryResult : object
            CSV-formatted  ``fr.inria.core.print.ResultFormat`` object.
        dtypes : list or dict, optional
            Optional column data types for the columns in the format as in ``panads.read_csv`` method.
            https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        Returns
        -------
        pd.DataFrame
            Corese object converted to a DataFrame.
        """
        assert self.ResultFormat, 'Corese classes are not loaded properly.'

        df = pd.read_csv(StringIO(str(queryResult)),
                            skipinitialspace=True,
                            dtype=dtypes)

        # Assign n/a to empty strings
        string_dtypes = df.convert_dtypes().select_dtypes("string")
        df[string_dtypes.columns] = string_dtypes.replace(r'^\s*$', None, regex=True)

        return df

    #TODO: add timeout parameter
    def sparqlConstruct(self, graph: Optional[object] = None,
                        query: str ='',
                        merge: bool=False)-> object:
        """
        Execute SPARQL CONSTRUCT query on Corese graph.

        Optionally the new triples can be merged with the existing graph.

        Parameters
        ----------
        graph : object, optional
            Corese ``fr.inria.corese.core.Graph`` object. If not provided (default), a new graph is created.
        query : str, optional
            SPARQL query. Defaults to an empty string, resulting in an empty graph.
        merge : bool, optional
            Option to merge the result with the existing graph passed in the parameters. Default is False.

        Returns
        -------
        object
            Result of the SPARQL CONSTRUCT query in RDF/XML format.
        """
        assert self.QueryProcess, 'Corese classes are not loaded properly.'
        assert self.ResultFormat, 'Corese classes are not loaded properly.'

        if not graph:
            graph = self.Graph()

        exec = self.QueryProcess.create(graph)
        map = exec.query(query)

        if merge:
            graph.getGraph().merge(map.getGraph())

        result = self.ResultFormat.create(map, self.ResultFormat.DEFAULT_CONSTRUCT_FORMAT)

        return result


    def toTurtle(self, rdf:object)-> str:
        """
        Convert RDF/XML to Turtle format.

        Parameters
        ----------
        rdf : object
            Corese RDF object

        Returns
        -------
        str
            RDF in Turtle format.
        """

        assert self.Transformer, 'Corese classes are not loaded properly.'

        # TODO: ASk Remi about getGraph, the Graph and the right way to do the transformation
        ttl = self.Transformer.create(rdf.getMappings().getGraph(), self.Transformer.TURTLE)

        return ttl.toString()

    #TODO: ASk Remi what are the acceptable shacl formats
    def shaclValidate(self, graph: object,
                      shacl_shape_ttl: str ='',
                      return_dataframe = False)-> str:
        """
        Validate RDF graph against SHACL shape.

        This version supports only Turtle format to define a SHACL shape.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        shacl_shape_ttl : str, optional
            SHACL shape in Turtle format. If not provided, the validation will be skipped.
        return_dataframe : bool, optional
            Return the validation report as a DataFrame. Default is False.

        Returns
        -------
        str
            SHACL validation report in Turtle format.
        """
        assert self.Shacl, 'Corese classes are not loaded properly.'

        shapeGraph = self.Graph()
        ld = self.Load.create(shapeGraph)

        if _isFile(shacl_shape_ttl):
            # Load shape graph from file
            ld.parse(shacl_shape_ttl)
        else:
            # Load shape graph from string
            ld.loadString(shacl_shape_ttl,
                          self.Loader.format.TURTLE_FORMAT)

        # Evaluation
        shacl = self.Shacl(graph.getGraph(), shapeGraph)
        result = shacl.eval()

        trans = self.Transformer.create(result, self.Transformer.TURTLE)

        if return_dataframe:
            return self.shaclReportToDataFrame(str(trans.toString()))

        return str(trans.toString())

    # Parse validation report
    def shaclReportToDataFrame(self, validation_report: str)-> pd.DataFrame:
        """
        Convert SHACL validation report to ``pandas.DataFrame``.

        Parameters
        ----------
        validation_report : str
            SHACL validation report in Turtle format.

        Returns
        -------
        pd.DataFrame
            Validation report as a DataFrame.
        """

        validation_report_graph = self.loadRDF(validation_report)

        report = self.sparqlSelect(validation_report_graph, self.SHACL_REPORT_QUERY)

        report = report.pivot(index='o', columns='p', values='s')
        report.columns = [uri.split('#')[-1] for uri in report.columns]

        report.reset_index(drop=True, inplace=True)

        return report

    #TODO: add a named graph  parameter
    def addTriple(self, graph: object, subject: str, predicate: str, obj: str)-> object:
        """
        Add a triple to the default Corese graph.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        subject : str
            Subject of the triple. Must be a URI.
        predicate : str
            Predicate of the triple. Must be a URI.
        obj : str
            Object of the triple. Must be a URI or a literal.

        Returns
        -------
        object
            Corese ``fr.inria.corese.core.Graph`` object with the new triple.
        """
        subject = graph.addResource(subject)
        predicate = graph.addProperty(predicate)

        if obj.startswith('http'):
            obj = graph.addResource(obj)
        else:
            obj = graph.addLiteral(obj)

        graph.addEdge(subject, predicate, obj)

        return graph

    def removeTriple(self, graph: object, subject: str, predicate: str, obj: str)-> object:
        """
        Remove a triple from the default Corese graph.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object
        subject : str
            Subject of the triple. Must be a URI.
        predicate : str
            Predicate of the triple. Must be a URI.
        obj : str
            Object of the triple. Must be a URI or a literal.

        Returns
        -------
        object
            Corese ``fr.inria.corese.core.Graph`` object without the triple.
        """
        subject = graph.getResource(subject)
        predicate = graph.getResource(predicate)

        if obj.startswith('http'):
            obj = graph.getResource(obj)
        else:
            obj = graph.getLiteral(obj)

        graph.delete(subject, predicate, obj)

        return graph

    def getTripleObject(self, graph, subject:str, predicate:str)->Optional[str]:
        """
        Get the object of a triple. It can be a URI or a literal.

        Parameters
        ----------

        Return
        ------
        str
            String representation of the object of the triple or None if the triple does not exist.
        """
        subject = graph.getResource(subject)
        predicate = graph.getResource(predicate)

        obj = graph.getEdgesRDF4J(subject, predicate, None, None)

        if obj.iterator().hasNext():
            return obj.iterator().next().getObjectNode().getLabel()

        return None

    def exportRDF(self, graph:object, path:str, format:str ='turtle', overwrite:bool=False)-> None:
        """
        Export Corese graph to an RDF file. Only RDF/XML and Turtle are supported by this version.

        Parameters
        ----------
        graph : object
            Corese ``fr.inria.corese.core.Graph`` object.
        path : str
            Path to the output RDF file.
        format : str, optional
            RDF format. Default is Turtle. Accepted values are
            *turtle*, *ttl*, *xml*, and *rdfxml*.

        overwrite : bool, optional
            Overwrite the file if it exists. Default is False.
        """

        format = format.lower()

        if 'xml' in format or 'rdf' in format:
            format = self.Transformer.RDFXML
        elif 'ttl' in format or 'turtle' in format:
            format = self.Transformer.TURTLE
        else:
            raise ValueError('Unsupported RDF format. Only RDF/XML and Turtle are supported by this version')

        if os.path.exists(path) and not overwrite:
            raise FileExistsError(f'{path} already exists. Set overwrite=True to overwrite the file.')

        transformer = self.Transformer.create(graph, format)
        transformer.write(path)

        #TODO: apply prefixes to the output file


if __name__ == "__main__":

    # Initialize the CoreseAPI
    cr = CoreseAPI(java_bridge='py4j')
    cr.loadCorese()

    # Load RDF file
    gr = cr.loadRDF(os.path.abspath(os.path.join('.', 'examples', 'data','beatles.rdf')))
    print("Graph size: ", gr.graphSize())

    # Load Rule Engine OwlRL
    ren = cr.loadRuleEngine(gr, profile=cr.RuleEngine.Profile.OWLRL)
    print("Graph size: ", gr.graphSize())

    # Load another Rule Engine e.g. RDFS to replace the existing one
    ren = cr.loadRuleEngine(gr, profile=cr.RuleEngine.Profile.RDFS, replace=True)
    print("Graph size: ", gr.graphSize())

    # Reset Rule Engine
    cr.resetRuleEngine(gr)
    print("Graph size: ", gr.graphSize())

    # Execute SPARQL SELECT query
    res = cr.sparqlSelect(gr, query='select * where {?s ?p ?o} limit 5')

    # Convert the result to DataFrame
    print(cr.toDataFrame(res))

    # Execute SPARQL CONSTRUCT query
    prefixes = ['@prefix ex: <http://example.com/>']
    contruct = '''CONSTRUCT {?Beatle a ex:BandMember }
                WHERE { ex:The_Beatles ex:member ?Beatle}'''
    results = cr.sparqlConstruct(gr, prefixes=prefixes, query=contruct)
    print(results)

    # Convert the result to Turtle
    print(cr.toTurtle(results))

    # Execute SHACL validation
    shacl_shape_file = '.\\examples\\data\\beatles-validator.ttl'
    report = cr.shaclValidate(gr, shacl_shape_ttl=shacl_shape_file, prefixes=prefixes)
    print(report)

    # Convert SHACL validation report to DataFrame
    shr = cr.shaclReportToDataFrame(report)
    print(shr)

    # Shutdown the JVM
    cr.unloadCorese()

    print("Done!")
