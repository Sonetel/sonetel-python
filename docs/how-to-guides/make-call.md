# How to make a phone call using Sonetel API.

In this tutorial, we will show you how to make a callback call using Sonetel's callback API.

## What is a callback?

In a callback, you provide us with two phone numbers. One number is where you can answer a call and the other one is of the person you wish to speak to. Instead of mobile numbers you can also provide SIP addresses or registered email addresses in case of Sonetel users.

Our system first calls you and when you answer, calls the other number or SIP address you provided. When the second call has been answered successfully, the calls will be connected together.

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
from sonetel import Auth, Call
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

### Make a callback call

Now, we will make a callback call using the `callback()` method of the `Call` class.

First we will create an instance of the `Call` class and then call the `callback()` method. The `callback()` method takes two parameters, the destination where you want to answer the first call and the destination you want to call.

In the following example, `my_sip_address@sip.example.com` is our SIP address where we want to receive the call. `+44123456789` is the number we want to call.
```python
call = Call(access_token)
response = call.callback(
    num1='my_sip_address@sip.example.com',
    num2='+44123456789'
)
```

### Check the response

We can check the response to see if the call was successful or not. If the call is succesful, we get a 202-accepted response with a session ID.

```python
if response['statusCode'] == 202:
    print(f'Call successful. Call ID: {response["response"]["session_id"]}')
else:
    print('Call failed')
```

A successful API response looks like this:
```json
{
  "statusCode": 202,
  "response": {
    "session_id": "1234567890"
  }
}
```

## Complete code

```python
import os
from sonetel import Auth, Call

user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

auth = Auth(user,pswd)
access_token = auth.get_access_token()

call = Call(access_token)
response = call.callback(num1='my_sip_address@sip.example.com', num2='+44123456789')

if response['statusCode'] == 202:
    print(f'Call successful. Call ID: {response["response"]["session_id"]}')
else:
    print('Call failed')
```