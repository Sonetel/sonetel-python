#!/bin/bash

sh setup.sh > /dev/null
sh -x run_tests.sh
sh cleanup.sh > /dev/null
