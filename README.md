# pycorese

pycorese is a python wrapper to the corese "Software platform for the Semantic Web of Linked Data"

Corese documentation:  https://corese-stack.github.io/corese-core/
Corese python wrapper: https://corese-stack.github.io/corese-python/


## Quick installation guide

## installation from pypi.org

- have or install python (3.10 minimal), preferably in a (pyenv or conda) virtual environement and runnable

```bash
pip install pycorese
```

- check the installation

```
python -c 'import pycorese ; print(pycorese.__version__)'
```


## compiling from sources (complete instructions in INSTALL.md)

- clone the package

```bash
git clone git@github.com:corese-stack/corese-python.git
```

- have also java installed (tested on openjdk 11)

- run the following commands:

```bash
./gradlew clean shadowJar
./gradlew downloadCoreseCore
mkdir ./resources
cp ./build/libs/*.jar ./resources/
pip install setuptools wheel build
python -m build
```

- test

```bash
./python_examples/simple_query.py
```

If anythong goes wrong, refer to the INSTALL.md file or to the documentation website.
