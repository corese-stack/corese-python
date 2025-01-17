.. pycorese documentation master file, created by
    sphinx-quickstart on Thu Oct 14 2023.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

.. image:: _static/corese.svg
   :align: center
   :width: 400px

.. centered:: Python API for Corese Semantic Web platform

.. Define named hyperlinks for the references of W3C standards
.. _Corese: corese.html
.. _corese-core: https://github.com/corese-stack/corese-core

.. _RDF: https://www.w3.org/RDF/
.. _RDFS: https://www.w3.org/2001/sw/wiki/RDFS
.. _SPARQL: https://www.w3.org/2001/sw/wiki/SPARQL
.. _OWL RL: https://www.w3.org/2005/rules/wiki/OWLRL
.. _SHACL: https://www.w3.org/TR/shacl/

`Corese`_ is a software platform implementing and extending the standards of the Semantic Web. It allows to create, manipulate, parse, serialize, query, reason, and validate RDF data. Corese is based on the W3C standards `RDF`_, `RDFS`_, `OWL RL`_, `SPARQL`_ and `SHACL`_. Corese is implemented as a set of open-source Java libraries.

**pycorese** is a Python package that provides a simple way to integrate the `corese-core`_ Java library into Python applications.

**pycorese** offers an intuitive API to interact with Corese's capabilities such as storage, SPARQL engine, RDFS and OWL reasoning, and SHACL validation.

**pycorese** unlocks the potential of Semantic Web stack for applications such as semantic data analysis, knowledge graph construction, and Machine Learning.

.. raw:: html

   <h3>Contributions and discussions</h3>


.. _discussion forum: https://github.com/corese-stack/corese-python/discussions/
.. _issue reports: https://github.com/corese-stack/corese-python/issues/
.. _pull requests: https://github.com/corese-stack/corese-python/pulls/

For support questions, comments, and any ideas for improvements you’d like to discuss, please use our `discussion forum`_. We welcome everyone to contribute to `issue reports`_, suggest new features, and create `pull requests`_.


.. #############################################################################
.. The statements below are to produce the title of the page in the tab
   and a menu with the links to the pages of the documentation

.. raw html below is used to hide the title of the page but retain it in the
   tab title. https://github.com/sphinx-doc/sphinx/issues/8356
.. raw:: html

   <div style="visibility: hidden;">

pycorese doc
===================================

.. raw:: html

   </div>

.. toctree::
   :maxdepth: 2
   :hidden:

   User Guide <user_guide.ipynb>
   API <python_api/index.rst>
   Install <dev_install.md>
   About Corese <corese.rst>
