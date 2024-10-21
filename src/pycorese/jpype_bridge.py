"""Implementation of the JPype bridge to Corese API in Java."""

import logging
import os
import sysconfig

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

from .corese_version import corese_version

class JPypeBridge:
    """
    Python wrapper of the Java Corese API using JPype bridge.

    Parameters
    ----------
    corese_path : str, optional
        Path to the Corese-core library. Default is None.
        if None, use the jar file provided by the package

        Remark: the CORESE_PATH environment variable can be used to
        provide enaltenative jar file.
    """

    def __init__(self,
                 corese_path=None):

        if corese_path:
            self.corese_path = corese_path
            if not os.path.exists(self.corese_path):
                msg = f'given CORESE library is not found at {self.corese_path}.'
                logging.critical(msg)
                raise FileNotFoundError('\n'+msg)

        else:
            package_jar_path = os.path.join(sysconfig.get_paths()['data'], 'share', 'pycorese', f'corese-core-{corese_version}-jar-with-dependencies.jar')
            self.corese_path = os.environ.get("CORESE_PATH", package_jar_path)

            if not os.path.exists(self.corese_path):
                msg = f'given CORESE library is not found at {self.corese_path}.'
                logging.critical(msg)
                raise FileNotFoundError('\n'+msg)

        self.java_gateway = None

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)

    def _exit_handler(self):
        jpype.shutdownJVM()
        logging.info('JPype: CORESE is stopped')

    def unloadCorese(self, force=False):
        """
        Explicitly unload Corese library.

        It's not necessary to call this method, as the library is automatically
        unloaded when the Python interpreter exits.
        """
        logging.info('JPype: WARNING: CORESE cannot be restarted after unloading.')

        if force:
            self._exit_handler()
            self.java_gateway = None
        else:
            logging.info('JPype: If the unloading is necessary run unloadCorese method with the force=True option')

    def loadCorese(self,  memory_allocation=None) -> jpype:
        """
        Load Corese library into context of JPype.

        Parameters
        ----------
        memory_allocation : str, optional
            Memory allocation for the JVM, e.g. '4g'. Default is automatic allocation by JVM.

        Returns
        -------

            jpype
            JPype object.
        """
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

            # This is a minimum set of classes required for the API to work
            # if we need more classes we should think about how to expose
            # them without listing every single one of them here

            # Import of class
            from fr.inria.corese.core import Graph # type: ignore
            from fr.inria.corese.core.load import Load  # type: ignore
            from fr.inria.corese.core.logic import RDF, RDFS  # type: ignore
            from fr.inria.corese.core.print import ResultFormat  # type: ignore
            from fr.inria.corese.core.query import QueryProcess  # type: ignore
            from fr.inria.corese.core.rule import RuleEngine  # type: ignore
            from fr.inria.corese.core.transform import Transformer # type: ignore

            from fr.inria.corese.core.storage.api.dataManager import DataManager  # type: ignore
            from fr.inria.corese.core.storage import CoreseGraphDataManager # type: ignore
            from fr.inria.corese.core.storage import CoreseGraphDataManagerBuilder  # type: ignore

            from fr.inria.corese.core.shacl import Shacl # type: ignore
            #from fr.inria.corese.core.api import Loader # type: ignore

            self.DataManager = DataManager
            self.CoreseGraphDataManager = CoreseGraphDataManager
            self.CoreseGraphDataManagerBuilder = CoreseGraphDataManagerBuilder

            self.Graph = Graph
            self.Load = Load
            self.QueryProcess = QueryProcess
            self.ResultFormat = ResultFormat
            self.RDF = RDF
            self.RDFS = RDFS
            self.RuleEngine = RuleEngine
            self.Transformer = Transformer

            self.Shacl = Shacl
            #self.Loader = Loader

            logging.info('JPype: CORESE is loaded')


        except Exception as e:
            logging.error('JPype: CORESE failed to load: %s', str(e))


        return jpype
