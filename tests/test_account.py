import pytest

from sonetel import Account
from sonetel import exceptions as e
from tests.common_functions import access_token

token = access_token()
if token:
    account = Account(access_token=token)
else:
    raise e.AuthException("Cannot get access token")


def test_account_init():
    assert account is not None


def test_account_get():
    response = account.get()
    assert response["status"] == "success"
    assert "name" in response["response"]


def test_account_get_accountid():
    accountid = account.get_accountid()
    assert isinstance(accountid, str)
    assert accountid == account._accountid


def test_account_get_balance():
    balance = account.get_balance()
    assert isinstance(balance, str)


def test_account_get_balance_with_currency():
    balance = account.get_balance(currency=True)
    assert isinstance(balance, str)
    assert " " in balance


def test_account_update_empty_body():
    response = account.update()
    assert response["status"] == "failed"


def test_account_get_with_fields():
    response = account.get(fields="usage")
    assert response["status"] == "success"
    assert "usage" in response["response"]
