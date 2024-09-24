"""The module provides the capability to launch corese-python jar."""
import pandas as pd
from io import StringIO

class CoreseAPI:
    """
    Python implementation of Corese API.

      :param bridge: Bridge name to use for Java integration ('py4j' or 'jpype'). Default is 'py4j'.
    """

    def __init__(self, java_bridge: str = 'py4j'):

        if java_bridge.lower() not in ['py4j', 'jpype']:
            raise ValueError('Invalid java bridge. Only "py4j" and "jpype" are supported.')

        self.java_bridge = java_bridge.lower()
        self.java_gateway = None

        self.Graph = None
        self.QueryProcess = None
        self.ResultFormat = None
        self.Load = None

    def loadCorese(self) -> None:
        """Load Corese library into JVM and expose the Corese classes."""
        if self.java_bridge == 'py4j':

            from .py4J_bridge import Py4JBridge

            py4j_bridge = Py4JBridge()
            self.java_gateway = py4j_bridge.loadCorese()

            # This is a minimum set of classes required for the API to work
            # if you need more classes we should think about how to expose
            # them without listing every single one of them here
            self.Graph = py4j_bridge.Graph
            self.Load = py4j_bridge.Load
            self.QueryProcess = py4j_bridge.QueryProcess
            self.ResultFormat = py4j_bridge.ResultFormat
            self.RDF = py4j_bridge.RDF
            self.RuleEngine = py4j_bridge.RuleEngine
            self.Transfomer = py4j_bridge.Transformer

            # Classes to manage Graph(s) with different storage options
            self.DataManager = py4j_bridge.DataManager
            self.CoreseGraphDataManager = py4j_bridge.CoreseGraphDataManager
            self.CoreseGraphDataManagerBuilder = py4j_bridge.CoreseGraphDataManagerBuilder

            self.Shacl  = py4j_bridge.Shacl
            self.Loader = py4j_bridge.Loader

        else:

            from .jpype_bridge import JPypeBridge

            jpype_bridge = JPypeBridge()
            self.java_gateway = jpype_bridge.loadCorese()


            self.Graph = jpype_bridge.Graph
            self.Load = jpype_bridge.Load
            self.QueryProcess = jpype_bridge.QueryProcess
            self.ResultFormat = jpype_bridge.ResultFormat
            self.RDF = jpype_bridge.RDF
            self.RuleEngine = jpype_bridge.RuleEngine
            self.Transfomer = jpype_bridge.Transformer

            # Classes to manage Graph(s) with different storage options
            self.DataManager = jpype_bridge.DataManager
            self.CoreseGraphDataManager = jpype_bridge.CoreseGraphDataManager
            self.CoreseGraphDataManagerBuilder = jpype_bridge.CoreseGraphDataManagerBuilder

            self.Shacl  = jpype_bridge.Shacl
            self.Loader = jpype_bridge.Loader


    def loadRDF(self, rdf_file: str, graph=None)-> object:
        """
        Load RDF file into Corese graph.

        Parameters
        ----------
        rdf_file : str
            Path to the RDF file.
        graph : object (fr.inria.corese.core.Graph or
                        fr.inria.corese.core.storage.CoreseGraphDataManager), optional
            Corese graph object. Default is None.

        Returns
        -------
        object (fr.inria.corese.core.Graph or fr.inria.core.storage.CoreseGraphDataManager)
            Corese Graph object.
        """
        if not self.java_gateway:
            self.loadCorese()

        assert self.Graph, 'Corese classes are not loaded properly.'
        assert self.Load, 'Corese classes are not loaded properly.'
        assert self.CoreseGraphDataManagerBuilder, 'Corese classes are not loaded properly.'

        if not graph:
            graph = self.Graph()

        graph_mgr = self.CoreseGraphDataManagerBuilder().build()

        ld = self.Load().create(graph, graph_mgr)
        ld.parse(rdf_file)

        return graph_mgr

    def loadRuleEngine(self, graph: object,
                        profile: object,
                        replace:bool = False)-> object:
            """
            Load rule engine for the given graph.

            Parameters
            ----------
            graph : object (fr.inria.corese.core.Graph or fr.inria.core.storage.CoreseGraphDataManager)
                Corese graph object or DataManager.
            profile : object
                Profile object for the rule engine. Accepted values:
                - RuleEngine.Profile.RDFS
                - RuleEngine.Profile.OWLRL
                - RuleEngine.Profile.OWLRL_LITE
                - RuleEngine.Profile.OWLRL_EXT
            replace : bool, optional
                Replace the existing rule engine. Default is False.

            Returns
            -------
            object (fr.inria.core.rule.RuleEngine)
                RuleEngine object.
            """
            assert self.RuleEngine, 'Corese classes are not loaded properly.'
            assert graph, 'Graph object is required.'
            assert profile, 'Profile object is required.'

            if replace:
                self.resetRuleEngine(graph)

            rule_engine = self.RuleEngine.create(graph)

            rule_engine.setProfile(profile)
            rule_engine.process()

            return rule_engine

    def resetRuleEngine(self, graph: object)-> None:
        """
        Reset the rule engine for the given graph.

        Parameters
        ----------
        graph : object (fr.inria.corese.core.Graph or fr.inria.core.storage.CoreseGraphDataManager)
            Corese graph object or DataManager.

        Returns
        -------
        None
        """
        assert self.RuleEngine, 'Corese classes are not loaded properly.'
        assert graph, 'Graph object is required.'

        rule_engine = self.RuleEngine.create(graph.getGraph())
        rule_engine.remove()

    def sparqlSelect(self, graph: object,
                    prefixes: str|list|None = None,
                    query: str ='SELECT * WHERE {?s ?p ?o} LIMIT 5')-> object:
        """
        Execute SPARQL SELECT or ASK query on Corese graph.

        Parameters
        ----------
        graph : object (fr.inria.corese.core.Graph)
            Corese graph object.
        prefixes : str or list
            SPARQL prefixes.
        query : str
            SPARQL query.

        Returns
        -------
        object (fr.inria.core.print.ResultFormat)
            Result of the SPARQL

        """
        assert self.QueryProcess, 'Corese classes are not loaded properly.'
        assert self.ResultFormat, 'Corese classes are not loaded properly.'

        if not graph:
            raise ValueError('Graph object is required.')

        if not prefixes:
            prefixes = ''
        if isinstance(prefixes, list):
            prefixes = '\n'.join(prefixes)

        exec = self.QueryProcess.create(graph)
        map = exec.query('\n'.join([prefixes, query]) )

        # to keep it simple for now return the result in CSV format
        result = self.ResultFormat.create(map, self.ResultFormat.SPARQL_RESULTS_CSV)

        return result

    def toDataFrame(self, queryResult: object,
                            dtypes: list|dict|None = None)-> pd.DataFrame:
        """
        Convert Corese ResultFormat object to pandas DataFrame.

        Parameters
        ----------
        queryResult : csv resultFormat object (fr.inria.core.print.ResultFormat)
            ResultFormat object.
        dtypes : list or dict, optional
            Data types for the columns in the format required by Pandas
            read_csv method https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html.
            Default is None.

        Returns
        -------
        pd.DataFrame
            Result in DataFrame format.
        """
        #assert isinstance(queryResult, self.ResultFormat), 'Invalid query result object.'

        df = pd.read_csv(StringIO(str(queryResult)),
                            skipinitialspace=True,
                            dtype=dtypes)

        # Assign n/a to empty strings
        string_dtypes = df.convert_dtypes().select_dtypes("string")
        df[string_dtypes.columns] = string_dtypes.replace(r'^\s*$', None, regex=True)

        return df

    def sparqlConstruct(self, graph, prefixes, query, merge=False):
        """
        Execute SPARQL CONSTRUCT query on Corese graph.

        Parameters
        ----------
        graph : object (fr.inria.corese.core.Graph)
            Corese graph object.
        prefixes : str or list
            SPARQL prefixes.
        query : str
            SPARQL query.
        merge : bool, optional
            Merge the result with the existing graph. Default is False.

        Returns
        -------
        object (fr.inria.core.print.ResultFormat)
            Result of the SPARQL
        """
        assert self.QueryProcess, 'Corese classes are not loaded properly.'
        assert self.ResultFormat, 'Corese classes are not loaded properly.'

        exec = self.QueryProcess.create(graph)
        map = exec.query('\n'.join([prefixes, query]) )

        if merge:
            graph.merge(map.getGraph())

        result = self.ResultFormat.create(map, self.ResultFormat.DEFAULT_CONSTRUCT_FORMAT)

        return result

    def shaclValidate(self, graph, shacl_shape_ttl, is_file_name=False):
        pass
    # Parse validation results
    def shaclValidationReport(self, validation_report_graph):
       pass
