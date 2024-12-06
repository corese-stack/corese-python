# Development Installation

This document describes how to install the development environment for the **pycorese** package.

**pycorese** is a Python wrapper for the [Corese-core](https://github.com/corese-stack/corese-core) Java library. To build and use this package, you need to have Java installed on your system.

**pycorese**  provides two options for running the Corese Java code using the following Python packages to access Java objects:

* [Py4J](https://www.py4j.org/)
* [JPype](https://jpype.readthedocs.io/en/latest/)

That's the reason the installation process is a bit more complex than for a standard Python package.

## Clone the GitHub repository

```bash
git clone https://github.com/corese-stack/corese-python.git
cd corese-python
```


## Python build environment

You can use the provided [conda](https://docs.conda.io/en/latest/) environment file to create a virtual environment with the necessary dependencies.

```bash
conda env update -f pkg/env/corese-python.yaml
conda activate corese-python
```
Or install the dependencies manually:

* project dependencies:
    ```bash
    pip install py4j jpype1 pandas
    ```
* build dependencies:
    ```bash
    pip install --upgrade pip setuptools wheel build
    ```
* test dependencies:
    ```bash
    pip install pytest pytest-cov
    ```
* documentation dependencies:
    ```bash
    pip install sphinx pydata_sphinx_theme
    ```

<!-- TODO: Add other documentation dependencies install support-->
<!-- TODO: Add conda install support-->

## Java build environment

To build the package Java Development Kit (JDK) version 11 or higher and the [Gradle](https://docs.gradle.org/current/userguide/userguide.html) build tool are required.

If Java is not installed, visit the [official website](https://www.java.com/en/download/help/download_options.html) for installation instructions.

Gradle can be installed as an extension to your IDE or as a standalone tool.

* Gradle extension for VSCode is available from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-gradle)

* To install Gradle as a standalone tool, follow the instructions on the [official website](https://gradle.org/install/).


## Building the package

Clean all the build directories (not necessary if you just downloaded the source code):

```
rm -fr dist build resources src/pycorese.egg-info
```

Build the package:

```
python -m build
```

This command builds the packages into `./dist` directory. Note that the custom `sdist` command is implemented in [setup.py](./setup.py).

The custom `sdist` command adds the following steps:

* compile the `corese-python-x.y.z-jar-with-dependencies.jar` file using the Gradle build tool. This jar file is required to run Corese using the `Py4J` bridge.
* download the `corese-core-x.y.z-jar-with-dependencies.jar` file from the Maven repository. This jar file is required to run Corese using the `JPype` bridge.
* copy the jar files to the `./resources` directory.



> [!NOTE]
> - do not run `python setup.py` that will not build the full package.
> - the versions of `pycorese`, `corese-python`, `corese-core` are maintained separately.
> -  the commands for the first two steps are provided in the [Obtaining Java libraries manually](#obtain-java-libraries-manually) section.

## Testing the package

From the top directory, or in the `./tests` sub-directory run the command:

```
pytest -v
```

If a specific test fails, you can have more information, using the following command:

```
pytest tests/test_api.py::Test_api::test_bad_bridge
```

> [!NOTE]
> - substitute the filename, test class name, and test name with your specific test.

Run the test coverage:

```
pytest --cov
```

For the HTML coverage report, run the following commands:

```
pytest --cov --cov-report=html
open htmlcov/index.html
```


## Installing the locally built package

```
pip install dist/pycorese-0.1.1-py3-none-any.whl
```

or
```
pip install dist/pycorese-0.1.1.tar.gz
```

## Verifying the installation

```
$ pip list  | grep corese
pycorese                  0.1.1

$ python -c 'import pycorese'
```
> [!NOTE]
> - change the version number accordingly.


## Run a simple example

Without installing the package you can run the following command (the default Java bridge is `py4j`):

```
./examples/simple_query.py -j $PWD/build/libs/corese-python-4.6.0-jar-with-dependencies.jar
```

or change the bridge to `jpype`:

```
./examples/simple_query.py -b jpype -j $PWD/build/libs/corese-core-4.6.0-jar-with-dependencies.jar
```

<!--  **_NOTE:_** -->
> [!NOTE]
> - the jar files are obtained either by [building the package](#building-the-package) or [manually](#obtain-java-libraries-manually).
> - the primary development focus is on using the `py4j` bridge.


## Obtain Java libraries manually

In case you want to build `corese-python-x.y.z-jar-with-dependencies.jar` Java library separately, use the following commands:

```
gradlew shadowJar
```

In case you want to download the `corese-core-x.y.z-jar-with-dependencies.jar` Java library separately, use the following commands:

```
gradlew downloadCoreseCore
```
These tasks are defined in the [build.gradle.kts](./build.gradle.kts) file.