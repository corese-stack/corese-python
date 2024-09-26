"""The module provides the capability to launch corese-python jar."""
import pandas as pd
from io import StringIO

class CoreseAPI:
    """
    Python implementation of Corese API.

      :param bridge: Bridge name to use for Java integration ('py4j' or 'jpype'). Default is 'py4j'.
    """

    def __init__(self, java_bridge: str = 'jpype'):
        
        if java_bridge.lower() not in ['py4j', 'jpype']:
            raise ValueError('Invalid java bridge. Only "py4j" and "jpype" are supported.')

        self.java_bridge = java_bridge.lower()
        self.java_gateway = None

        self.Graph = None
        self.QueryProcess = None
        self.ResultFormat = None
        self.Load = None

    def unloadCorese(self):
        """
        Explicitly unload Corese library.
        
        It's not necessary to call this method, as the library is automatically
        unloaded when the Python interpreter exits.

        WARNING: After unloading Corese bridged by JPype it is not possible to restart it.
        """
        self._bridge.unloadCorese()

    def loadCorese(self) -> None:
        """Load Corese library into JVM and expose the Corese classes."""
        if self.java_bridge == 'py4j':
           
            from .py4J_bridge import Py4JBridge

            self._bridge = Py4JBridge()
            self.java_gateway = self._bridge.loadCorese()
        else:

            from .jpype_bridge import JPypeBridge

            self._bridge = JPypeBridge()
            self.java_gateway =self._bridge.loadCorese()


            # self.Graph = jpype_bridge.Graph
            # self.Load = jpype_bridge.Load
            # self.QueryProcess = jpype_bridge.QueryProcess
            # self.ResultFormat = jpype_bridge.ResultFormat
            # self.RDF = jpype_bridge.RDF
            # self.RuleEngine = jpype_bridge.RuleEngine
            # self.Transformer = jpype_bridge.Transformer

            # # Classes to manage Graph(s) with different storage options
            # self.DataManager = jpype_bridge.DataManager
            # self.CoreseGraphDataManager = jpype_bridge.CoreseGraphDataManager
            # self.CoreseGraphDataManagerBuilder = jpype_bridge.CoreseGraphDataManagerBuilder

            # self.Shacl  = jpype_bridge.Shacl
            # self.Loader = jpype_bridge.Loader

        # This is a minimum set of classes required for the API to work
        # if you need more classes we should think about how to expose
        # them without listing every single one of them here
        self.Graph = self._bridge.Graph
        self.Load = self._bridge.Load
        self.QueryProcess = self._bridge.QueryProcess
        self.ResultFormat = self._bridge.ResultFormat
        self.RDF = self._bridge.RDF
        self.RuleEngine = self._bridge.RuleEngine
        self.Transformer = self._bridge.Transformer
        
        # Classes to manage Graph(s) with different storage options
        self.DataManager = self._bridge.DataManager
        self.CoreseGraphDataManager = self._bridge.CoreseGraphDataManager
        self.CoreseGraphDataManagerBuilder = self._bridge.CoreseGraphDataManagerBuilder

        self.Shacl  = self._bridge.Shacl
        self.Loader = self._bridge.Loader
        
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
                    query: str ='SELECT * WHERE {?s ?p ?o} LIMIT 5',
                    return_dataframe: bool =True)-> object:    
        """ 
        Execute SPARQL SELECT or ASK query on Corese graph.
        
        Parameters
        ----------
        graph : object (fr.inria.corese.core.Graph)
            Corese graph object.
        prefixes : str or list
            SPARQL prefixes. Default is None.
        query : str
            SPARQL query. Default is 'SELECT * WHERE {?s ?p ?o} LIMIT 5'.
        return_dataframe : bool, optional. Default is True. 
        
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

        if return_dataframe:
            return self.toDataFrame(result)

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

    #TODO: add timeout
    def sparqlConstruct(self, graph: object,
                        prefixes: str|list|None = None,
                        query: str ='',
                        merge: bool=False)-> object:
        """
        Execute SPARQL CONSTRUCT query on Corese graph.

        Optionally the new triples can be merged with the existing graph.

        Parameters
        ----------
        graph : object (fr.inria.corese.core.Graph)
            Corese graph object.
        prefixes : str or list
            SPARQL prefixes. Default is None.
        query : str
            SPARQL query. Default is empty string resulting in empty graph.
        merge : bool, optional
            Merge the result with the existing graph. Default is False.

        Returns
        -------
        object (fr.inria.core.print.ResultFormat)
            Result of the SPARQL CONSTRUCT query in RDF?XML format.
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

        if merge:
            graph.getGraph().merge(map.getGraph())
        
        result = self.ResultFormat.create(map, self.ResultFormat.DEFAULT_CONSTRUCT_FORMAT)

        return result

    def toTurtle(self, rdf:object)-> str:
        """
        Convert RDF/XML to Turtle format.

        Parameters
        ----------
        rdf : object (fr.inria.corese.core.Graph)
            Corese graph object.

        Returns
        -------
        str
            RDF in Turtle format.
        """
        assert self.Transformer, 'Corese classes are not loaded properly.'

        # TODO: ASk Remi about getGraph, the Graph and the right way to do the transformation
        ttl = self.Transformer.create(rdf.getMappings().getGraph(), self.Transformer.TURTLE)
        
        return ttl.toString()

    def shaclValidate(self, graph, shacl_shape_ttl, is_file_name=False):
        pass
    # Parse validation results
    def shaclValidationReport(self, validation_report_graph):
       pass


if __name__ == "__main__":

    # Initialize the CoreseAPI
    cr = CoreseAPI(java_bridge='jpype')
    cr.loadCorese()

    # Load RDF file
    gr = cr.loadRDF('C:\\Users\\abobashe\\Documents\\P16\\PyCorese\\examples\\data\\beatles.rdf')
    print("Graph size: ", gr.graphSize())

    # Load Rule Engine OwlRL
    re = cr.loadRuleEngine(gr, profile=cr.RuleEngine.Profile.OWLRL)
    print("Graph size: ", gr.graphSize())

    # Load another Rule Engie e.g. RDFS to replace the existing one
    re = cr.loadRuleEngine(gr, profile=cr.RuleEngine.Profile.RDFS, replace=True)
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

    # Execute SHACL validation report

    # Shutdown the JVM
    cr.unloadCorese()

    print("Done!")
