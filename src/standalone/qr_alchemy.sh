#!/bin/bash

BASEDIR=$(dirname $0)

cd "$BASEDIR"/../..

export PYTHONPATH=%BUILD_LIB%
exec %BUILD_BIN%/qr_alchemy -c %BUILD_CONF%/qr_alchemy.conf -p %BUILD_SHARE% "$@"
