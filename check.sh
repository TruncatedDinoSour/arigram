#!/bin/sh

set -ex

echo Checking and formatting with black...
black --check arigram/

echo Python type checking...
mypy arigram --warn-redundant-casts --warn-unused-ignores \
    --no-warn-no-return --warn-unreachable --strict-equality \
    --ignore-missing-imports --warn-unused-configs \
    --disallow-untyped-calls --disallow-untyped-defs \
    --disallow-incomplete-defs --check-untyped-defs \
    --disallow-untyped-decorators --pretty --show-traceback \
    --no-warn-unused-ignores --follow-imports=error --namespace-packages \
    --python-version "$(head -n1 runtime.txt)"

echo Checking import sorting...
isort -c arigram/*.py

echo Checking unused imports...
flake8 --select=F401
