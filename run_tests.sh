#!/usr/bin/env bash

TESTS=$(echo $(ls test/[^.]*_test.py) | sed -e "s/\//./g" | sed -e "s/\.py//g")
echo "Running tests: $TESTS"
python -m unittest $TESTS
