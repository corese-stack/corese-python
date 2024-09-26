# local tests with py4j

## remark

at the moment, the jar file is tagged as '5.0.0-SNAPSHOT'

## build jar file locally

```
./gradlew clean publishToMavenLocal
```

## Conda environment

For conda users: 
```bash
conda env update -f pkg/env/corese-python.yaml
conda activate corese-python
```
Makes available the python libraries: `pandas`, `py4j`, `jpype1`, `maven-artifact`.

## test py4j bridge example in python

```
./python_examples/simple_query.py -j $PWD/build/libs/corese-python-5.0.0-SNAPSHOT-jar-with-dependencies.jar
```


## test jpype bridge example in python

May work but not garanteed !!!

```
./python_examples/simple_query.py -b jpype -j /somewhere/corese-core-5.0.0-SNAPSHOT-jar-with-dependencies.jar
```

#
