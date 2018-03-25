#!/bin/bash

export PYTHONPATH=.

# Making directories for output files
mkdir -p .tmp/integration_test/lib/util/author/
mkdir -p .tmp/integration_test/lib/util/graph/
mkdir -p .tmp/integration_test/lib/input/data_cleanup/
mkdir -p .tmp/integration_test/lib/analysis/author/graph/generate/
mkdir -p .tmp/integration_test/lib/analysis/author/ranking/
mkdir -p .tmp/integration_test/lib/analysis/author/wh_table/

py.test -v --color=yes --cov=.
codecov
