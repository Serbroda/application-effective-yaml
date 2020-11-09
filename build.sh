#!/bin/sh

rm -rf ./target
mkdir -p ./target
mkdir -p ./target/build

python3 -m pip install -r requirements.txt --target ./target/build
cp -a ./app/. ./target/build/

python3 -m zipapp target/build -o ./target/application_effective_yaml.pyz
