# Changelog

All notable changes to the Sonetel Python Module are tracked in this file.

## [0.2.1] - 24-08-2024
### Added
- `delete()` method added to the VoiceApp class. Can be used to delete an existing voice app in the account.

### Fixed
- `get()` method in the Recording class didn't apply the optional parameters correctly. Fixed now.

## [0.2.0] - 26-04-2023
### Added

- Separate API endpoints.
- Check if number is in E164 format before using it in any API request.
- return a dict with status, message and error code if the inputs to a methods are invalid or missing.
- Fetch call recordings
- Load common strings from constants.py
- Common functions moved to utilities.py
- Wherever possible, classes support standard get, add, update and delete methods.
- Allow users to update some account information.
- Add account ID and user ID to the callback app name.

## [0.1.5] - 11-08-2022
### Fixed
+ Issue #1: add audience parameter to decode token function.

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
