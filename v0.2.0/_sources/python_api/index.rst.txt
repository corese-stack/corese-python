.. .. currentmodule:: pycorese


Python API Reference
===================================

**pycorese** is a Python wrapper for accessing and manipulating RDF data with Corese features connected by one of the Java bridge packages: ``py4j`` or ``jpype``.

.. note::

    **pycorese** is still in beta version and is under active development. The API may change in future releases.


In the following sections, you will find the documentation of the Python API of **pycorese**.

High-level API
--------------

HIgh-level API is a set of convenience methods to facilitate the common tasks of working with Knowledge Graphs.

.. automodule:: pycorese.api
   :members:  CoreseAPI
   :undoc-members:
   :member-order: bysource



.. contents::
   :local:
   :depth: 2

Low-level API
-------------

Low-level API is a subset of ``corese-core`` classes exposed as Python objects. These are dynamically created classes
and can be accessed only after the Corese engine is loaded

For the details of these classes and their methods, please refer to the `Corese Java documentation <https://corese-stack.github.io/corese-core/v4.6.0/java_api/library_root.html>`_.

.. autoattribute:: pycorese.api.CoreseAPI.Graph
   :annotation:

   Corese ``fr.inria.corese.core.Graph`` object.

.. autoattribute:: pycorese.api.CoreseAPI.Load
   :annotation:

   Corese ``fr.inria.corese.core.load.Load`` object.

.. autoattribute:: pycorese.api.CoreseAPI.QueryProcess
   :annotation:

   Corese ``fr.inria.corese.core.query.QueryProcess`` object.

.. autoattribute:: pycorese.api.CoreseAPI.ResultFormat
   :annotation:

   Corese ``fr.inria.corese.core.print.ResultFormat`` object.

.. autoattribute:: pycorese.api.CoreseAPI.RuleEngine
   :annotation:

   Corese ``fr.inria.corese.core.rule.RuleEngine`` object.

.. autoattribute:: pycorese.api.CoreseAPI.Transformer
   :annotation:

   Corese ``fr.inria.corese.core.transform.Transformer`` object.

.. autoattribute:: pycorese.api.CoreseAPI.Shacl
   :annotation:

   Corese ``fr.inria.corese.core.shacl.Shacl`` object.


.. toctree::
   :maxdepth: 2

   About Java bridges <bridges.rst>