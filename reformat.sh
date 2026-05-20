#!/bin/sh

set -e

cd $(dirname $0)

if ! test -d .venv
then
python3 -m venv .venv
fi

. .venv/bin/activate

pip3 install isort ruff
echo 'running isort:'
isort .
echo 'running ruff:'
ruff check . --fix
ruff format .

echo
echo done
