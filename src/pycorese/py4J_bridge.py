"""Implementation of the Py4J bridge to Corese API in Java."""


import os
import subprocess
from time import sleep
from importlib import resources
from pathlib import Path
import logging

from py4j.java_gateway import JavaGateway

import pycorese.maven_tools as pmt


class Py4JBridge:
    """
    Manage running Corese-Python Java library using Py4J.

    Parameters
    ----------
    corese_path : str, optional
        Path to the Corese-Python library. Default is None.
        If None, download the default version (5.0.0) from maven
        If provided, use it instead of maven versions (useful for debug)
    version: str, optional
        version which will be downloaded

    """

    def __init__(self,
                 corese_path: str|None =None,
                 version: str = "5.0.0"):

        if corese_path:
            self.corese_path = corese_path
            if not os.path.exists(corese_path):
                msg = f'given CORESE library is not found at {corese_path}.'
                logging.critical(msg)
                raise FileNotFoundError(
                    '\n'+msg)

        else:
            # use maven to load the jar file
            self.corese_path = pmt.package2filename("corese-python",
                                                    version)

            if not os.path.exists(self.corese_path):
                pmt.maven_download("corese-python",
                                   version)

        self.java_gateway = None

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)

    def _exit_handler(self) -> None:
        if self.java_gateway is not None:
            self.java_gateway.shutdown()
            logging.info('Py4J: CORESE is stopped')

    def unloadCorese(self):
        """
        Explicitly unload Corese library.

        It's not necessary to call this method, as the library is automatically
        unloaded when the Python interpreter exits.
        """
        self._exit_handler()
        self.java_gateway = None

    def loadCorese(self,  memory_allocation=None) -> JavaGateway:
        """Load Corese-Python library in the context of Py4J.

        Parameters
        ----------
        memory_allocation : str, optional
            Memory allocation for the JVM, e.g. '4g'. Default is automatic allocation by JVM.

        Returns
        -------
        JavaGateway
            Py4J JavaGateway object.
        """
        # restart JVM if is already runningS
        if self.java_gateway is not None:
            self.java_gateway.shutdown()
            logging.info('Py4J: Stopped JVM with CORESE...')

        try:
            logging.info('Py4J: Loading CORESE...')

            java_args = ['-Dfile.encoding=UTF8']
            if memory_allocation:
                java_args.extend(f'-Xmx{memory_allocation}')

            print(f"DEBUG= {self.corese_path}")
            self.java_gateway = JavaGateway.launch_gateway(classpath=str(self.corese_path),
                                                            javaopts=java_args,
                                                            die_on_exit=True)
            #sleep(1.0)


            # This is a minimum set of classes required for the API to work
            # if we need more classes we should think about how to expose
            # them without listing every single one of them here

            self.Graph = self.java_gateway.jvm.fr.inria.corese.core.Graph
            print(f"DEBUG= {self.Graph}")
            self.Load = self.java_gateway.jvm.fr.inria.corese.core.load.Load
            self.QueryProcess = self.java_gateway.jvm.fr.inria.corese.core.query.QueryProcess
            self.ResultFormat = self.java_gateway.jvm.fr.inria.corese.core.print.ResultFormat
            self.RDF = self.java_gateway.jvm.fr.inria.corese.core.logic.RDF
            self.RuleEngine = self.java_gateway.jvm.fr.inria.corese.core.rule.RuleEngine
            self.Transformer = self.java_gateway.jvm.fr.inria.corese.core.transform.Transformer

            self.DataManager = self.java_gateway.jvm.fr.inria.corese.core.storage.api.dataManager.DataManager
            self.CoreseGraphDataManager = self.java_gateway.jvm.fr.inria.corese.core.storage.CoreseGraphDataManager
            self.CoreseGraphDataManagerBuilder = self.java_gateway.jvm.fr.inria.corese.core.storage.CoreseGraphDataManagerBuilder

            self.Shacl  = self.java_gateway.jvm.fr.inria.corese.core.shacl.Shacl
            self.Loader = self.java_gateway.jvm.fr.inria.corese.core.api.Loader


            logging.info('Py4J: CORESE is loaded')

        except Exception as e:
            logging.error('Py4J: CORESE failed to load: %s', str(e))

        return self.java_gateway
