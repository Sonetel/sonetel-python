<br />
<div align="center">
  <a href="https://github.com/Sonetel/sonetel-python">
    <img src="https://dl.dropboxusercontent.com/s/hn4o0v378od1aoo/logo_white_background.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Sonetel Python SDK</h3>

<p align="center">
    Python package for using Sonetel's REST API endpoints.
    <br />
    <br />
    <a href="https://sonetel.com/en/developer/">Sonetel Developer Home</a>
    .
    <a href="https://sonetel.com/en/developer/api-documentation/">API Documentation</a>
    .
    <a href="https://app.sonetel.com/register?tag=api-developer&simple=true">Get Free Account</a>
  </p>
</div>

![GitHub](https://img.shields.io/github/license/sonetel/sonetel-python) &nbsp; ![PyPI](https://img.shields.io/pypi/v/sonetel) &nbsp; ![GitHub issues](https://img.shields.io/github/issues/sonetel/sonetel-python) &nbsp; [![Documentation Status](https://readthedocs.org/projects/sonetel-python/badge/?version=latest)](https://sonetel-python.readthedocs.io/en/latest/?badge=latest)

## 1. Introduction
The Sonetel API is a REST based web-service that enables you to manage your Sonetel account from your own platform or service. You can manage your account, your phone numbers and make callback calls etc.

This Python package provides an easy-to-use interface to integrate Sonetel's APIs with your service. For more information about the API, please see the [documentation](https://docs.sonetel.com/).

## 2. Get Started

To use the package, you need a Sonetel account. If you don't already have one, get a free account from <a href="https://app.sonetel.com/register?tag=api-developer&simple=true">sonetel.com</a>.

### 2.1 Installation

#### 2.1.1 PIP

This is the recommended way to install the module. It installs the latest stable version from the Python Package Index.

`pip install sonetel`

#### 2.1.2 Git

To get the latest features, clone [the repository](https://github.com/Sonetel/sonetel-python) and [follow these instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to build the SDK locally.

### 2.2 Usage

To use the package, add the following line to the top of your Python program.

`import sonetel`

Here's a description of the various modules and the methods available with each.
#### 2.2.1 Auth

The Auth module is used to generate and manage access tokens.

To instantiate it, you need to pass your Sonetel username and password to it. It supports the following methods:

1. `create_token()` - create a new access token. Called automatically when a new instance is created.
2. `get_access_token()` - fetch the current access token.
3. `get_refresh_token()` - get the refresh token, used to refresh the access token.
4. `get_decoded_token()` - return the decoded JWT value. Returns a dict.

##### Generate an access token

```python
import os
import sonetel as sntl

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sntl.Auth(username=user, password=pswd)

print(s.get_access_token())
```

#####  Refresh access token

When your access token has expired, you can use the `create_token()` method to get a new `access_token` & `refresh_token`.

This automatically updates the Account object to use the newly generated access and refresh tokens.

```python
import os
import sonetel as sntl

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sntl.Auth(username=user, password=pswd)

print(s.get_access_token())

# Generate the refresh token and update the Account object
response = s.create_token(refresh="yes", grant_type="refresh_token")

print(response)
```

##### Get decoded JWT token

Get the decoded JWT token.

```python
import os
import sonetel as sntl

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sntl.Auth(username=user, password=pswd)

print(s.get_decoded_token())

```

#### 2.2.2 Account

The Account module provides you information about your Sonetel account. For example, the prepaid balance, address and so on.

It supports the following methods:

1. `get()` - Get information about the account. Return a dict with an overview of the information such as account ID, currency, prepaid balance, country and so on.
2. `update()` - Update basic information about your account.
3. `get_balance()` - Returns the prepaid balance. Pass the parameter `currency` = `True` to include the currency with the returned value.
4. `get_accountid()` - Fetch the account ID.

##### Print your Sonetel account ID and the current prepaid balance.

```python
import os
from sonetel import Auth
from sonetel import Account

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = Auth(username=user,password=pswd)

a = Account(s.get_access_token())

print(f"Your account ID is {a.get_accountid()} and your prepaid balance is {a.get_balance()}.")
```

#### 2.2.3 Call

Use this to make callback calls with your Sonetel account.

It supports the `callback()` method which requires your mobile number and the number of the person you wish to speak to. In a callback call, our system will first call you and when you answer, call the other number you provided. When the second call has been answered successfully, the calls will be connected together.

##### Make a callback call

When making a callback call, `num1` is the destination where you will first answer the call before we call `num2`. This can be your mobile number, a SIP address or your Sonetel email address.

If you set `num1` as your Sonetel email address, then the call will be handled as per your incoming call settings.

```python
import os
import sonetel

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sonetel.Auth(username=user,password=pswd)

c = sonetel.Call(s.get_access_token())

result = c.callback(
    num1="YOUR_NUMBER_OR_ADDRESS",
    num2="NUMBER_TO_CALL",
)
print(result)
```

#### 2.2.4 Phone Number

The `Phonenumber` module allows you to manage phone numbers in your Sonetel account.

It supports the following methods:

1. `get()` - get a list of phone numbers in your account. By default only returns a list of the E164 numbers. Set the parameter `e164only` equal to `False` to get detailed information.
2. `add()` - buy a new phone number.
3. `update()` - update the call forwarding settings for a phone number.
4. `delete()` - remove a phone number from your Sonetel account.

##### List the phone numbers available in your account

```python
import os
import sonetel

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sonetel.Auth(username=user,password=pswd)

ph = sonetel.PhoneNumber(s.get_access_token())
print(ph.get())

```

## Storing your credentials

Please keep your Sonetel login credentials safe to avoid any misuse of your account. Do not hard code them into scripts or save them in files that are saved in any form of version control.

You can add them to your operating system's environment variables and use Python's `os` module to fetch them.

Assuming the username and password are stored in environment variables named `sonetelUsername` and `sonetelPassword` respectively, here's how you can access them from a script:

```python
import os
import sonetel

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

s = sonetel.Auth(username=user,password=pswd)

print(s.get_access_token())
```

## Help

For help with the Sonetel API, have a look at the <a href="https://docs.sonetel.com">API documentation</a>.

If you have an issue with the module, please [report an issue](https://github.com/Sonetel/sonetel-python/issues/issues) on GitHub.
