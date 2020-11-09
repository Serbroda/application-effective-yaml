#!/bin/sh

mkdir ./target
python3 -m zipapp app -m "main:main" -o ./target/application_effective_yaml.pyz
