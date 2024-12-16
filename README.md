<div align="center">
  <h2>pycorese</h2>
</div>

<!-- Short description -->
<p align="center">
   Python API for CORESE Semantic Web platform
</p>

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/pypi/pyversions/pycorese.svg" alt="Python Versions">
  <a href="https://pypi.org/project/pycorese/"><img src="https://img.shields.io/pypi/v/pycorese?color=informational" alt="PyPI version"></a>
  <a href="https://corese-stack.github.io/corese-python/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue" alt="Documentation"></a>
  <a href="https://codecov.io/gh/corese-stack/pycorese"><img src="https://codecov.io/gh/corese-stack/pycorese/branch/master/graph/badge.svg" alt="codecov"></a>
  <a href="https://opensource.org/licenses/LGPL-3.0"><img src="https://img.shields.io/badge/License-LGPL-yellow.svg" alt="License: LGPL"></a>
</p>

<!-- Long description -->

 [Corese](https://corese-stack.github.io/corese-core) is a software platform implementing and extending the standards of the Semantic Web. It allows to create, manipulate, parse, serialize, query, reason, and validate RDF data. Corese is based on the W3C standards RDF, RDFS, OWL 2, SPARQL and SHACL. Corese is implemented as a set of open-source Java libraries.

**pycorese** is a Python package that provides a simple way to integrate the [corese-core](https://github.com/corese-stack/corese-core) Java library into Python applications.

**pycorese** offers an intuitive API to interact with Corese's capabilities such as storage, SPARQL engine, RDFS and OWL reasoning, and SHACL validation.

**pycorese** unlocks the potential of Semantic Web stack for applications such as semantic data analysis, knowledge graph construction, and Machine Learning.

## Installation

**pycorese** can be easily installed via `pip`:

```bash
pip install pycorese
```

This process installs both the Python wrappers and the Corese Java libraries. To run the Java libraries, ensure that Java is installed on your system. A Java Runtime Environment (JRE) version 11 or higher is required. If Java is not installed, visit the [official website](https://www.java.com/en/download/help/download_options.html) for installation instructions.

<!-- TODO: conda installation-->

## Development installation

To install **pycorese** from the current [GitHub repository](https://github.com/corese-stack/corese-python) follow the instructions from [INSTALL.md](https://github.com/corese-stack/corese-python/blob/main/INSTALL.md).

## Usage

Here is a simple example of how to use **pycorese** to load and query RDF data:

```python
from  pycorese.api import CoreseAPI

corese = CoreseAPI()
corese.loadCorese()

# Load RDF data
data = """
@prefix ex: <http://example.org/> .
ex:John ex:hasFriend ex:Jane, ex:Jill.
ex:Jane ex:age 25 .
ex:Jill ex:age 40 .
"""

graph = corese.loadRDF(data)

# Query the data to find out who is John's younger friend
query = """
PREFIX ex: <http://example.org/>
SELECT ?friend ?age
WHERE {
    ?x ex:age ?ageX .
    ?x ex:hasFriend ?friend .
    ?friend ex:age ?age .
    FILTER (?ageX > ?age)
}
"""

results = corese.sparqlSelect(graph, query=query, return_dataframe=True)
print(results)
```
Expected output:
```
                    friend  age
0  http://example.org/Jane   25
```

See the [GitHub repository]((https://github.com/corese-stack/corese-python/examples)) for more examples.

## Documentation

- pycorese GitHub pages:  https://corese-stack.github.io/corese-python
- Corese GitHub pages: https://corese-stack.github.io/corese-core


## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please [open an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) or [submit a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) on the [GitHub repository](https://github.com/corese-stack/corese-python).
