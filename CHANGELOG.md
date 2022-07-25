# Changelog

All notable changes to the Sonetel Python Module are tracked in this file.

## [0.1.2] - 25-07-2022

### Changes
+ Fix issue in `subscription_listnums()` that doesn't return anything when `e164only=False`. 

## [0.1.1] - 22-07-2022

### Added
+ Updated docstring for `callback()`.
+ Add `__init__.py` to main folder for a simpler `import` statement.
+ `get_userid()` - return the user ID of the user whose credentials are used to create the token.

### Changes
+ Rename `account_id()` to `get_accountid()`.
+ Rename `account_balance()` to `get_balance()`.
+ Minor code optimization

## [0.1.0] - 15-07-2022

### Changes

+ First public release
