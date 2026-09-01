import pytest

from sonetel import Call
from sonetel import exceptions as e
from tests.common_functions import access_token

token = access_token()
if token:
    call = Call(access_token=token)
else:
    raise e.AuthException("Cannot get access token")


def test_call_init():
    assert call is not None


def test_call_init_rejects_short_app_name():
    with pytest.raises(e.SonetelException):
        Call(access_token=token, app_name="x")


def test_callback_requires_both_numbers():
    response = call.callback(num1="", num2="+44123456789")
    assert response["status"] == "failed"

    response = call.callback(num1="+12125551234", num2="")
    assert response["status"] == "failed"
