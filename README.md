<br />
<div align="center">
  <a href="https://github.com/Sonetel/sonetel-python">
    <img src="https://dl.dropboxusercontent.com/s/hn4o0v378od1aoo/logo_white_background.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Sonetel API Python Wrapper</h3>

<p align="center">
    A simple Python wrapper for using Sonetel's REST API endpoints.
    <br />
    <br />
    <a href="https://sonetel.com/en/developer/">Sonetel Developer Home</a>
    .
    <a href="https://sonetel.com/en/developer/api-documentation/">API Documentation</a>
    .
    <a href="https://app.sonetel.com/register?tag=api-developer&simple=true">Get Free Account</a>
  </p>
</div>

## Introduction
The Sonetel API is a REST based web-service that enables you to manage your Sonetel account from your own platform or service. You can manage your account, your phone numbers and make callback calls etc.

This is a simple python wrapper to use Sonetel's communication APIs. For more information about the API, please see the [documentation](https://docs.sonetel.com/).

## Getting Started

To use the module, you need a Sonetel account. If you don't already have one, get a free account from <a href="https://app.sonetel.com/register?tag=api-developer&simple=true">sonetel.com</a>.

### Installation

#### PIP
Run the following command to install from pip.

`pip install sonetel`

#### Git
To get the latest features, clone a specific [tag](https://github.com/Sonetel/sonetel-python/issues/tags) and [follow these instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to build the module locally.

## Functions

The following functions are support at the moment. More will be added in the future.

- `get_balance()` - Get the prepaid balance of the account (e.g. '10'). Pass the argument `currency=True` to get the balance with the currency appended (e.g. '10 USD')
- `get_accountid()` - Returns your Sonetel account ID.
- `account_info()` - Fetch information about your account such as company name, balance, country, timezone, daily limit and so on.
- `account_users()` - Details of all the users in your account.
- `callback()` - Use our Callback API to make a callback call.
- `create_token()` - Create a new access token. A new access token is automatically created when you call the Account resource the first time.
- `get_token()` - Get the access token being used.
- `get_username()` - Returns the email address of the user that was used to create the token.
- `subscription_buynum()` - Purchase a phone number. Requires a phone number to be passed. Use the `/availablephonenumber` API endpoint to see a list of phone numbers available for purchase from a country and area.
- `subscription_listnums()` - See the details of all the phone numbers purchased by you. Pass the parameter `e164only=True` to only get a list of E.164 numbers without any metadata.

## Examples

### 1. Create an access token

```python
import os
from sonetel import api

user = os.environ.get('sonetelUserName')
pswd = os.environ.get('sonetelPassword')

s = api.Account(username=user,password=pswd)

print(s.get_token())
```

### 2. Print your Sonetel account ID and the current prepaid balance. 

```python
import os
from sonetel import api

user = os.environ.get('sonetelUserName')
pswd = os.environ.get('sonetelPassword')

s = api.Account(username=user,password=pswd)

print(f"Your account ID is {s.get_accountid()} and your prepaid balance is {s.get_balance()}.")
```

### 3. List the phone numbers available in your account

```python
import os
from sonetel import api

user = os.environ.get('sonetelUserName')
pswd = os.environ.get('sonetelPassword')

s = api.Account(username=user,password=pswd)

print(s.subscription_listnums(e164only=True))
```

### 4. Make a callback call

When making a callback call, `num1` is the destination where you will first answer the call before we call `num2`. This can be your mobile number, a SIP address or your Sonetel email address. 

If you set `num1` as your Sonetel email address, then the call will be handled as per your incoming call settings.

```python
import os
from sonetel import api

user = os.environ.get('sonetelUserName')
pswd = os.environ.get('sonetelPassword')

s = api.Account(username=user,password=pswd)

result = s.callback(
    num1="YOUR_NUMBER_OR_ADDRESS",
    num2="NUMBER_TO_CALL",
)
print(result)
```

## Storing your credentials

Please keep your credentials safe to avoid any misuse of your account. Do not hard code them into scripts or save them in files that are saved in any form of version control.

You can add them to your operating system's environment variables and use Python's `os` module to fetch them.

Assuming the username and password are stored in environment variables named `sonetelUserName` and `sonetelPassword` respectively, here's how you can access them from a script:

```python
import os
from sonetel import api

user = os.environ.get('sonetelUserName')
pswd = os.environ.get('sonetelPassword')

s = api.Account(username=user,password=pswd)

print(s.get_accountid())
```

## Help

For help with the Sonetel API, have a look at the <a href="https://docs.sonetel.com">API documentation</a>.

If you have an issue with the module, please [report an issue](https://github.com/Sonetel/sonetel-python/issues/issues) on GitHub.