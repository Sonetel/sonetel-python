import jwt
import requests
from time import time
from . import constants as const
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

def is_valid_token(decoded_token: dict) -> bool:
    """
    Return True if token hasn't expired. Accepts a decoded token.
    """
    # TODO: If token has expired, try to refresh it
    return decoded_token['exp'] - int(time()) > 60

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
                     bodyType: str = const.CONTENT_TYPE_GENERAL) -> dict:
    """
    Send an API request
    """

    # Checks
    if not token:
        raise e.SonetelException('"token" is a required parameter')
    if not uri:
        raise e.SonetelException('"uri" is a required parameter')

    # Prepare the request Header
    request_header = {
        "Authorization": "Bearer " + token,
        "Content-Type": bodyType,
        "User-Agent": f'Sonetel Python Package - v{const.PKG_VERSION}'
    }

    # Send the request
    r = requests.request(
        method=method,
        url=uri,
        headers=request_header,
        data=body
    )

    if r.status_code == requests.codes.ok:
        response = r.json()
        return response
    else:
        print(r.json())
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
