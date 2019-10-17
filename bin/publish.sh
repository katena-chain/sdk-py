#!/usr/bin/env bash

PROJECT_PATH=$(dirname $(cd $(dirname $0) && pwd))

cd ${PROJECT_PATH}
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf ${PROJECT_PATH}/.eggs
rm -rf ${PROJECT_PATH}/build
rm -rf ${PROJECT_PATH}/dist
rm -rf ${PROJECT_PATH}/katena_chain_sdk_py.egg-info