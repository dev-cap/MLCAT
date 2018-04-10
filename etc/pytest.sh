#!/bin/bash

export PYTHONPATH=.

set -ex

# Making directories for output files
mkdir -p .tmp/integration_test/lib/util/author/
mkdir -p .tmp/integration_test/lib/util/graph/
mkdir -p .tmp/integration_test/lib/input/data_cleanup/
mkdir -p .tmp/integration_test/lib/analysis/author/graph/generate/
mkdir -p .tmp/integration_test/lib/analysis/author/ranking/
mkdir -p .tmp/integration_test/lib/analysis/author/wh_table/
mkdir -p .tmp/integration_test/lib/analysis/author/edge_list/
mkdir -p .tmp/integration_test/lib/analysis/author/community/vertex_clustering/
mkdir -p .tmp/integration_test/lib/analysis/author/graph/interaction/

py.test -v --color=yes --cov=.
codecov
