# how to build/test/install pycorese java gateway and python wrapper from sources

## build/install the python package

### prerequesite

```
pip install --upgrade pip setuptools wheel build
```

### clean all (not necessary if your just downloaded the sources)

```
rm -fr dist build resources
```

### build the package

```
python -m build
```

which build the packages into `./dist`

Remark:
- do not run `python setup.py` which will not build the full package
- the described install process will:

 1/ compile the `corese-python-4.x.y-jar-with-dependencies.jar` file
 2/ download the `corese-core-4.x.y-jar-with-dependencies.jar` file from maven

- these two files are necessary to run the wrappers and are part of the distribution

### test

From the top directory, or in the `tests` sub-directory

```
pip install pytest
```

```
pytest -v
```

If a specific test fails, you can have more information, using:
(you need to know the filename, test class name, test name)

eg:
```
pytest tests/test_api.py::Test_api::test_bad_bridge
```

### code coverage

Install the coverage package:

```
pip install pytest-cov
```

And run the test coverage:

```
pytest --cov
```

If you prefer a browsable coverage report:

```
pytest --cov --cov-report=html
open htmlcov/index.html
```


### install the locally built package

```
pip install dist/pycorese-1.0.1-py3-none-any.whl
```

or
```
pip install dist/pycorese-1.0.1.tar.gz
```

- verify your installation

```
$ pip list  | grep corese
pycorese                  1.0.1

$ python -c 'import pycorese'
```

## Appendix 1: run local python example

### Conda environment

If necessary, we provide a conda environment:

```bash
conda env update -f pkg/env/corese-python.yaml
conda activate corese-python
```

This makes available the python libraries: `pandas`, `py4j`, `jpype1`

### run a simple example using py4j bridge (without installing)

```
./python_examples/simple_query.py -j $PWD/build/libs/corese-python-4.6.0-jar-with-dependencies.jar
```

Remark: to build this jar file, you must follow the Appendix 2 instructions

### experimental: run a simple example using jpype bridge (without installing)

We focus the development on the py4j wrapping. The (still provided) jpype interface
may still work (without garanty):

```
./python_examples/simple_query.py -b jpype -j /somewhere/corese-core-4.6.0-jar-with-dependencies.jar
```


## Appendix 2: java compilation description

Remark: all these commands are launched then building/installing using the previous described process

### build jar file locally

```
./gradlew shadowJar
```

### download

```
./gradlew downloadCoreseCore
```
