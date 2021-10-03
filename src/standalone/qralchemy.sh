#!/bin/bash

BASEDIR=$(dirname $0)

cd "$BASEDIR"/../..

export PYTHONPATH=%BUILD_LIB%
exec %BUILD_BIN%/qralchemy -c %BUILD_CONF%/qralchemy.conf -p %BUILD_SHARE% "$@"
