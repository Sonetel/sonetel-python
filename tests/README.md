# Testing

## Start

1. Build the package using `python -m build`
2. Install the package using pip from the `dist` directory. 
3. Install pytest if not already installed
4. Run all tests using `pytest`

## Prerequisites

### Sonetel Account
In order to test a Sonetel account is needed with the following setup:
- At least 2 users.
- Prepaid credit to test phone number purchase.
- A couple of recorded phone calls to test the call recording module

> Note: To test the User module, a new user is added to the Sonetel account and then deleted. This can incur charges if you are on a paid plan.

### Environment Variables

Set the following environment variables. These are used in unit tests.

- `SonetelUsername` - The email address of a Sonetel account
- `SonetelPassword` - Passsword for the above Sonetel account
- `SonetelSelfUserId` - Unique ID of your own user account in Sonetel.
- `SonetelTestUserId` - Unique ID of another user in your Sonetel account.