#!/bin/bash

echo "** SETUP ENVIRONMENT **"

cp ../dist/sonetel-*.tar.gz .
python3 -m venv tests
source tests/bin/activate
pip --disable-pip-version-check install sonetel-*.tar.gz

echo "** STARTING TESTS **"
python3 tests.py

echo "** TESTS FINISHED. RUN CLEANUP **"
rm -rf tests/
rm sonetel-*.tar.gz

echo "** ALL DONE **"
