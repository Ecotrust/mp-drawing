#!/bin/bash
PROJECT_NAME=$1
MODULE_NAME=mp-drawing

PROJECT_DIR=/usr/local/apps/$PROJECT_NAME
VIRTUALENV_DIR=$PROJECT_DIR/env
MODULE_DIR=$PROJECT_DIR/apps/$MODULE_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

$PIP install -r $MODULE_DIR/requirements.txt

$PYTHON $PROJECT_DIR/marineplanner/manage.py migrate
$PYTHON $PROJECT_DIR/marineplanner/manage.py enable_sharing --all
