# application-effective-yaml

[![license](https://img.shields.io/github/license/Serbroda/application-effective-yaml.svg)](https://github.com/Serbroda/application-effective-yaml/blob/master/LICENSE.txt)

A simple python app to merge multiple yamls files to get the effective content.

The intention to develop was to view the effectively used properties by a spring java applaction which uses multiple yaml based config locations.

## Key Features

* merge multiple local yaml files to get effective properties
* get and merge yaml files even inside a jar file
* export yaml files from a jar file

## Requirements

This app is designed to run on both major python versions:

* Python 2.7 or
* Python 3.x

## Installation

### From source

https://github.com/Serbroda/application-effective-yaml

```
git clone https://github.com/Serbroda/application-effective-yaml.git
cd application-effective-yaml
sudo python setup.py install
```

## Usage

Some simple examples:

```shell script
# get content of two merged yamls
application-effective-yaml.py -f test1.yml,test2.yml

# get content of two files inside a jar
application-effective-yaml.py -j ./test.jar:application.yml,./test.jar:application-test.yml

# get content of a file inside a jar and local file and extract the file from jar
application-effective-yaml.py -j ./test.jar:application.yml -f ./test1.yml -e

# extract a file from a jar to the sub directory test
application-effective-yaml.py -j ./test.jar:application.yml -e -o ./test/
```

Example output:

```yaml
application:
  msg: hello from test1.yml
app:
  msg: good morning
  name: John
  roles:
  - test1
  - test2
  permissions: []
onther-key:
  test: true
```
## Arguments

```
  -c DIRECTORY, --cwd DIRECTORY
                        current working directory
  -h, --help            show this help message end exit
  -f FILE_LIST, --files FILE_LIST
                        comma separated list of yaml files. order matters!
  -j FILE_IN_JAR_LIST, --jar-files FILES_IN_JAR_LIST
                        comma separated list of yaml files specified inside a jar (e.g test.jar:application.yml). order matters!
  -e, --extract         extracts the files specified in -j argument
  -o DIRECTORY, --out-dir DIRECTORY
                        output directory to extract the files in (default=cwd)
```
