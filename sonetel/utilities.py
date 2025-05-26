"""
Utilities for internal use
"""

import datetime
import logging
from time import time

import jwt
import requests

from . import _constants as const
from . import exceptions as e
from .session import SessionManager

# Configure logging
logger = logging.getLogger(__name__)

# Global session manager instance
_session_manager = None


def get_session(**kwargs) -> SessionManager:
    """
    Get or create the global session manager instance.

    Args:
        **kwargs: Optional configuration parameters for SessionManager

    Returns:
        The global SessionManager instance
    """
    global _session_manager
    if _session_manager is None or kwargs:
        _session_manager = SessionManager(**kwargs)
    return _session_manager


class Resource:
    """
    Base recource class for Sonetel API
    """

    def __init__(self, access_token: str):

        if not access_token:
            raise e.AuthException("access_token is a required parameter.")
        self._token: str = access_token
        self._decoded_token = decode_token(self._token)
        self._accountid: str = self._decoded_token["acc_id"]
        self._userid: str = self._decoded_token["user_id"]

        if not is_valid_token(self._decoded_token):
            raise e.AuthException("Token has expired")


# Static methods


def is_valid_token(decoded_token: dict) -> bool:
    """
    Return True if token hasn't expired. Accepts a decoded token.
    """
    # TODO: If token has expired, try to refresh it
    return decoded_token["exp"] - int(time()) > 60


def is_valid_date(date_text):
    """
    Check if the passed date is in the correct format
    """
    # Based on https://stackoverflow.com/a/16870699/18276605
    try:
        datetime.datetime.strptime(date_text, "%Y%m%dT%H:%M:%SZ")
        return True
    except Exception:
        return False


def date_diff(start, end):
    """
    Check if the end date is greater than start date. Returns a boolean.
    """
    start_date = datetime.datetime.strptime(start, "%Y%m%dT%H:%M:%SZ").strftime("%s")
    end_date = datetime.datetime.strptime(end, "%Y%m%dT%H:%M:%SZ").strftime("%s")
    return int(end_date) - int(start_date) > 0


def decode_token(token) -> dict:
    """
    Decode the JWT token
    """
    return jwt.decode(
        token, audience="api.sonetel.com", options={"verify_signature": False}
    )


def send_api_request(
    token: str,
    uri: str,
    method: str = "GET",
    body: str = "",
    body_type: str = const.CONTENT_TYPE_GENERAL,
) -> dict:
    """
    Send an API request to Sonetel using the session manager.

    Args:
        token: Required. String. The access token.
        uri: Required. String. The API endpoint to send the request to.
        method: Optional. String. The HTTP method to use. Defaults to GET.
        body: Optional. String. The body of the request. Defaults to an empty string.
        body_type: Optional. String. The content type of the body. Defaults to application/json.

    Returns:
        A dictionary containing the response.
    """

    # Checks
    if not token:
        raise e.SonetelException('"token" is a required parameter')
    if not uri:
        raise e.SonetelException('"uri" is a required parameter')

    # Get the session manager and send the request
    session = get_session()
    return session.request(
        method=method, url=uri, token=token, body=body, content_type=body_type
    )


def prepare_error(code: int, message: str) -> dict:
    """
    Prepare a dict with the error response.
    """
    return {"status": "failed", "code": code, "message": message}
