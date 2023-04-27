"""
Utilities for internal use
"""
from time import time
import datetime
import jwt
import requests
from . import _constants as const
from . import exceptions as e

class Resource:
    """
    Base recource class for Sonetel API
    """
    def __init__(self, access_token: str):

        if not access_token:
            raise e.AuthException("access_token is a required parameter.")
        self._token: str = access_token
        self._decoded_token = decode_token(self._token)
        self._accountid: str = self._decoded_token['acc_id']
        self._userid: str = self._decoded_token['user_id']

        if not is_valid_token(self._decoded_token):
            raise e.AuthException("Token has expired")

# Static methods

def is_valid_token(decoded_token: dict) -> bool:
    """
    Return True if token hasn't expired. Accepts a decoded token.
    """
    # TODO: If token has expired, try to refresh it
    return decoded_token['exp'] - int(time()) > 60

def is_valid_date(date_text):
    """
    Check if the passed date is in the correct format
    """
    # Based on https://stackoverflow.com/a/16870699/18276605
    try:
        datetime.datetime.strptime(date_text, '%Y%m%dT%H:%M:%SZ')
        return True
    except Exception:
        return False

def date_diff(start, end):
    """
    Check if the end date is greater than start date. Returns a boolean.
    """
    start_date = datetime.datetime.strptime(start, '%Y%m%dT%H:%M:%SZ').strftime('%s')
    end_date = datetime.datetime.strptime(end, '%Y%m%dT%H:%M:%SZ').strftime('%s')
    return int(end_date) - int(start_date) > 0

def decode_token(token) -> dict:
    """
    Decode the JWT token
    """
    return jwt.decode(
        token,
        audience='api.sonetel.com',
        options={"verify_signature": False}
    )


def send_api_request(token: str,
                     uri: str,
                     method: str = 'GET',
                     body: str = None,
                     body_type: str = const.CONTENT_TYPE_GENERAL) -> dict:
    """
    Send an API request to Sonetel.

    :param token: Required. String. The access token.
    :param uri: Required. String. The API endpoint to send the request to.
    :param method: Optional. String. The HTTP method to use. Defaults to GET.
    :param body: Optional. String. The body of the request. Defaults to None.
    :param body_type: Optional. String. The content type of the body. Defaults to application/json.
    :return: A dictionary containing the response.
    """

    # Checks
    if not token:
        raise e.SonetelException('"token" is a required parameter')
    if not uri:
        raise e.SonetelException('"uri" is a required parameter')

    # Prepare the request Header
    request_header = {
        "Authorization": "Bearer " + token,
        "Content-Type": body_type,
        "User-Agent": f'Sonetel Python Package - v{const.PKG_VERSION}'
    }

    # Send the request
    try:
        r = requests.request(
            method=method,
            url=uri,
            headers=request_header,
            data=body,
            timeout=60
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'status': 'failed', 'error': 'HTTPError', 'message': err.response.text}
    except requests.exceptions.ConnectionError as err:
        return {'status': 'failed', 'error': 'ConnectionError', 'message': err}
    except requests.exceptions.RequestException as err:
        return {'status': 'failed', 'error': 'RequestException', 'message': err}

    # pylint: disable=no-member
    if r.status_code == requests.codes.ok:
        return r.json()

    r.raise_for_status()

def prepare_error(code: int, message: str) -> dict:
    """
    Prepare a dict with the error response.
    """
    return {
        'status': 'failed',
        'code': code,
        'message': message
    }
