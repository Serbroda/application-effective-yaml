# application-effective-yaml

[![license](https://img.shields.io/github/license/Serbroda/application-effective-yaml.svg)](https://github.com/Serbroda/application-effective-yaml/blob/master/LICENSE.txt)

A simple python script to merge multiple yaml files to get the effective content.

The intention to develop this script was to view the effectively used properties by a spring java applaction which uses multiple yaml based config locations.

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
sudo ./build.sh
```

## Usage

Some simple examples:

```shell script
# get content of two merged yamls and write to result.yml
application-effective-yaml.py -f test1.yml,test2.yml -o result.yml

# get content of two files inside a jar
application-effective-yaml.py -j ./test.jar:application.yml,./test.jar:application-test.yml

# get content of a file inside a jar and local file and extract the file from jar
application-effective-yaml.py -j ./test.jar:application.yml -f ./test1.yml -e

# extract a file from a jar to the sub directory test
application-effective-yaml.py -j ./test.jar:application.yml -e -t ./test/
```

## Real world example

Command:
````shell script
application-effective-yaml.py -j my-test-app.jar:application.yml -f application-prod.yml  
````

Yaml inside a spring-boot jar:
```yaml
spring:
  application:
    name: my-test-app
  datasource:
    username: sa
    password:
    url: jdbc:h2:mem:test
    driver-class-name: org.h2.Driver

application:
  welcome-msg: Hello world
```
<small style="color: grey;">my-test-app.jar:application.yml</small>

Yaml to overwrite properties in production profile:
```yaml
spring:
  profiles: production
  datasource:
    username: mysql_prod
    password: S3cret!
    url: jdbc:mysql://localhost:3306/test
    driver-class-name: com.mysql.jdbc.Driver
```
<small style="color: grey;">application-prod.yml</small>

Result: 

```yaml
spring:
  application:
    name: my-test-app
  datasource:
    username: mysql_prod
    password: S3cret!
    url: jdbc:mysql://localhost:3306/test
    driver-class-name: com.mysql.jdbc.Driver
  profiles: production
application:
  welcome-msg: Hello world
```

## Command line arguments

```
  -c DIRECTORY, --cwd DIRECTORY
                        current working directory
  -h, --help            show this help message end exit
  -f FILE_LIST, --files FILE_LIST
                        comma separated list of yaml files. Order matters!
  -j FILE_IN_JAR_LIST, --jar-files FILES_IN_JAR_LIST
                        comma separated list of yaml files specified inside a jar (e.g test.jar:application.yml). Order matters!
  -o FILE, --out FILE   create output file with merged results
  -e, --extract         extracts the files specified in -j argument
  -t DIRECTORY, --target-dir DIRECTORY
                        target directory to extract the files in (default=cwd)
  -s, --strict-order    by default the jar files will always be taken before the local files. If the strict-order is set the files which are passed first will merge first
  -i, --ignore-errors   ignore errors like file not found
```
