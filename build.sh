#!/bin/bash

cd $(dirname $0)

if [ -n "$1" ]; then
  export RELEASE_TAG="$1"
fi

cargo build --release
