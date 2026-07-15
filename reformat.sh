#!/bin/sh

set -e

cd $(dirname $0)

if command -v cargo >/dev/null 2>&1
then
echo 'running cargo fmt:'
cargo fmt
fi

echo
echo done
