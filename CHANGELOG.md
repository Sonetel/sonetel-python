# Changelog

All notable changes to the Sonetel Python Module are tracked in this file.

## [0.1.4] - 26-07-2022
### Added
+ `get_voiceapps()` - get a detailed list of all the voice apps in a Sonetel account.
+ `get_decodedtoken()` - returns the decoded value of the JWT token.

### Changes
+ Update `create_token()` to refresh the access token easily.
+ Minor code optimization

## [0.1.3] - 25-07-2022
### Added
+ `get_refreshtoken()` - returns the refresh token if defined otherwise returns `False`.

### Changes
+ The project moves to its new [home](https://github.com/Sonetel/sonetel-python). The documentation has been updated to reflect this change.
+ `account_info()` now only returns the actual response, other metadata isn't returned.

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
