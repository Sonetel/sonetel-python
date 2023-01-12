#!/bin/bash

echo "** SETUP ENVIRONMENT **"

cp ../dist/sonetel-*.tar.gz .
python3 -m venv pyson
sleep 5
. pyson/bin/activate
pip --disable-pip-version-check install sonetel-*.tar.gz
python3 tests.py
rm -rf pyson/
rm sonetel-*.tar.gz