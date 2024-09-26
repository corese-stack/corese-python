# local tests with py4j

## remark

at the moment, the jar file is tagged as '5.0.0-SNAPSHOT'

## build jar file locally

```
./gradlew clean build
```

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
