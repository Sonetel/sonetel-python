# Testing

## Start

1. `cd` into the `tests` directory
2. Run `python setup.py install`
3. Install Pytest if not already installed
4. Run all tests using `pytest`

## Prerequisites

### Sonetel Account
In order to test a Sonetel account is needed with the following setup:
- At least 2 users.
- Prepaid credit to test phone number purchase.

### Environment Variables

Set the following environment variables. These are used in unit tests.

- `SonetelUsername` - The email address of a Sonetel account
- `SonetelPassword` - Passsword for the above Sonetel account
- `SonetelSelfUserId` - Unique ID of your own user account in Sonetel.
- `SonetelTestUserId` - Unique ID of another user in your Sonetel account.