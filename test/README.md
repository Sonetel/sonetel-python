# Testing

## Environment

At the moment the test environment is setup using Bash scripts. If you're using Windows for development, use the Windows Subsystem for Linux.

## Start

1. Build the module using `python3 -m build`.
2. `cd` into the `tests` directory
2. Start the automated tests using `sh run_tests.sh`

**Note**: Remember to have the `sonetelUsername` and `sonetelPassword` environment variables setup before running the tests.