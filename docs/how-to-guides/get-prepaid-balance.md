# Get Prepaid balance

In this guide, we will learn how to get the prepaid balance of your Sonetel account using the Sonetel API.

## Prerequisites

- Python 3.6 or higher
- Sonetel account
- `sonetel-python` package
- A mobile number or SIP address to call
- A number to call from

## Getting started

### Install the package

Install the `sonetel` package using `pip` if you don't already have it installed.
```bash
pip install sonetel
```

### Import the required packages

Import the packages we need.

The os package is used to get the username and password from the environment variables. This is a good practice to avoid hardcoding your credentials in your code.

```python
import os
from sonetel import Auth, Account
```

### Authenticate

Now, we will authenticate with Sonetel using our username and password.

The `Auth` class takes two parameters, the username and password. The `get_access_token()` method can then be used to get an access token. This token is required to make API calls.


```python
user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

auth = Auth(user,pswd)

access_token = auth.get_access_token()
```

### Get prepaid balance

Now, we will get the prepaid balance using the `get_balance()` method of the `Account` class.

```python
account = Account(access_token)
print("The current prepaid balance is: ", account.get_balance())
```

**Output:**
```
The current prepaid balance is:  1.23
```

#### With currency
To get the balance including the currency, set the `currency` flag to true.

```python
account = Account(access_token)
print("The current prepaid balance is: ", account.get_balance(currency=True))
```

**Output:**
```
The current prepaid balance is:  1.23 USD
```

## Complete code

```python
import os
from sonetel import Auth, Account

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

auth = Auth(user,pswd)
access_token = auth.get_access_token()

account = Account(access_token)
print("The current prepaid balance is: ", account.get_balance())
```