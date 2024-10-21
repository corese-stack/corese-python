# how to build/test/install pycorese java gateway and python wrapper

## remark

at the moment, the jar file is tagged as '5.0.0-SNAPSHOT'

## java part: build jar file locally

```
./gradlew clean publishToMavenLocal
```

or (jar file **must** be complete then loaded by python wrappers
```
./gradlew shadowJar
```

## python part: test locally

### Conda environment

For conda users:
```bash
conda env update -f pkg/env/corese-python.yaml
conda activate corese-python
```

Makes available the python libraries: `pandas`, `py4j`, `jpype1`

### run the tests

From the top directory, or in the `tests` sub-directory

```
pytest -v
```

If a specific test fails, you can have more informaiton, using:
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

And run the tests

```
pytest --cov
```

If you want a browsable coverage report:

```
pytest --cov --cov-report=html
open htmlcov/index.html
```

### run a simple example using py4j bridge (without installing)

```
./python_examples/simple_query.py -j $PWD/build/libs/corese-python-5.0.0-SNAPSHOT-jar-with-dependencies.jar
```

Remark: to build this jar file, you must run `./gradlew shadowJar` before

### experimental: run a simple example using jpype bridge (without installing)

May work but not garanteed !!! You need a corese-core jar file **with dependancies** !!!

```
./python_examples/simple_query.py -b jpype -j /somewhere/corese-core-5.0.0-SNAPSHOT-jar-with-dependencies.jar
```

## python installation

### prerequesite

```
pip install --upgrade pip setuptools wheel build
```

### build the package

```
python -m build
```

which build the packages into `./dist`


### install locally

```
pip install dist/pycorese-0.0-py3-none-any.whl
```

or
```
pip install dist/pycorese-0.0.tar.gz
```

- verify

```
$ pip list  | grep corese
pycorese                  0.0

$ python -c 'import pycorese'
```
