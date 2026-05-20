#!/bin/bash

cd $(dirname $0)

cd build

pyinstaller --clean ../app.spec
