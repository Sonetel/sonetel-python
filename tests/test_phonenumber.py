import pytest

from sonetel import PhoneNumber
from sonetel import exceptions as e
from sonetel.phonenumber import is_e164
from tests.common_functions import access_token

token = access_token()
if token:
    phone_number = PhoneNumber(access_token=token)
else:
    raise e.AuthException("Cannot get access token")


def test_is_e164_accepts_valid_numbers():
    assert is_e164("+12125551234") is True
    assert is_e164("12125551234") is True


def test_is_e164_rejects_invalid_numbers():
    assert is_e164("not-a-number") is False
    assert is_e164("123") is False


def test_phonenumber_init():
    assert phone_number is not None


def test_phonenumber_get():
    response = phone_number.get()
    assert response["status"] == "success"


def test_phonenumber_get_invalid_number():
    response = phone_number.get(number="not-a-number")
    assert response["status"] == "failed"
    assert response["code"] == 1000


def test_phonenumber_add_invalid_number():
    response = phone_number.add(number="not-a-number")
    assert response["status"] == "failed"
    assert response["code"] == 1000


def test_phonenumber_delete_invalid_number():
    response = phone_number.delete(number="not-a-number")
    assert response["status"] == "failed"
    assert response["code"] == 1000


def test_phonenumber_update_missing_number():
    response = phone_number.update(number="", connect_to_type="user", connect_to="x")
    assert response["status"] == "failed"


def test_phonenumber_update_missing_connect_to():
    response = phone_number.update(
        number="+12125551234", connect_to_type="user", connect_to=""
    )
    assert response["status"] == "failed"


def test_phonenumber_update_invalid_connect_to_type():
    response = phone_number.update(
        number="+12125551234", connect_to_type="bogus", connect_to="x"
    )
    assert response["status"] == "failed"


def test_phonenumber_country():
    response = phone_number.country(country="GBR")
    assert response["status"] == "success"
    assert response["response"]["name"] == "United Kingdom"
    assert response["response"]["phonenumbers"]


def test_phonenumber_stock_summary():
    # Boston (857) is known to carry select-order stock.
    response = phone_number.stock_summary("USA", area_code="857")
    assert response["status"] == "success"
    assert isinstance(response["response"], list)


def test_phonenumber_available_numbers():
    response = phone_number.available_numbers("USA", area_code="857")
    assert response["status"] == "success"
    assert response["response"]
    assert "phnum" in response["response"][0]
