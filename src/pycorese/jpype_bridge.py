"""Implementation of the JPype bridge to Corese API in Java."""

import logging
import os

from importlib import resources
from pathlib import Path

# Importing jpype.imports enables the functionality to import Java classes as 
# if they were Python modules, e.g. from fr.inria.corese.core import Graph
# Importing all classes from jpype.types enables the functionality to use Java
# types in Python, e.g. JArray, JClass, JBoolean, JByte, JChar, JShort, JInt, 
#                       JLong, JFloat, JDouble, JString, JObject, JException
# https://jpype.readthedocs.io/en/latest/userguide.html#importing-java-classes

import jpype
import jpype.imports
from jpype.types import *

#from . import configure_logging
#configure_logging()


_CORESE_LIBRARY_PATH = Path(resources.files(__package__))\
                       .joinpath('jars/corese-core-4.5.0-jar-with-dependencies.jar')\
                       .resolve()

class JPypeBridge:
    """
    Python wrapper of the Java Corese API using JPype bridge.

    Parameters
    ----------
    corese_path : str, optional
        Path to the Corese-core library. Default is None. If None, use the library 
        downloaded during package installation.
  
    """

    def __init__(self, corese_path=None): 

        self.corese_path = corese_path or (_CORESE_LIBRARY_PATH)

        if not os.path.exists(self.corese_path):
            raise FileNotFoundError(
                '\n'.join([f'CORESE library is not found at {self.corese_path}.',
                           f'Reinstall the {__package__} package.'])
            )

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)
       
    def _exit_handler(self):
        jpype.shutdownJVM()
        logging.info('CORESE is stopped')
		
    def loadCorese(self,  memory_allocation=None) -> jpype:
        """Load Corese library into context of JPype."""  
        # NOTE: Because of lack of JVM support, you cannot shutdown the JVM and then restart it.
        # Nor can you start more than one copy of the JVM.
        # https://jpype.readthedocs.io/en/latest/install.html#known-bugs-limitations

        try:
            # check if JVM is already running
            if jpype.isJVMStarted():
                logging.info('JPype: JVM is already running')
            else:
                logging.info('JPype: Loading CORESE...')
                java_args = ['-Dfile.encoding=UTF8']
                if memory_allocation:
                    java_args.append(f'-Xmx{memory_allocation}')
                jpype.startJVM(*java_args , classpath=[self.corese_path])


            # Import of class
            from fr.inria.corese.core import Graph # type: ignore
            from fr.inria.corese.core.load import Load  # type: ignore
            from fr.inria.corese.core.logic import RDF  # type: ignore
            from fr.inria.corese.core.print import ResultFormat  # type: ignore
            from fr.inria.corese.core.query import QueryProcess  # type: ignore
            from fr.inria.corese.core.rule import RuleEngine  # type: ignore
            from fr.inria.corese.core.transform import Transformer # type: ignore

            from fr.inria.corese.core.storage.api.dataManager import DataManager  # type: ignore
            from fr.inria.corese.core.storage import CoreseGraphDataManager  # type: ignore
            from fr.inria.corese.core.storage import CoreseGraphDataManagerBuilder  # type: ignore

            from fr.inria.corese.core.shacl import Shacl # type: ignore
            from fr.inria.corese.core.api import Loader # type: ignore
            
            self.DataManager = DataManager
            self.CoreseGraphDataManager = CoreseGraphDataManager
            self.CoreseGraphDataManagerBuilder = CoreseGraphDataManagerBuilder
            
            self.Graph = Graph
            self.Load = Load
            self.QueryProcess = QueryProcess
            self.ResultFormat = ResultFormat
            self.RDF = RDF
            self.RuleEngine = RuleEngine
            self.Transformer = Transformer
            
            self.Shacl = Shacl
            self.Loader = Loader

            logging.info('JPype: CORESE is loaded')


        except Exception as e:
            logging.error('JPype: CORESE failed to load: %s', str(e)) 
     

        return jpype
    

		