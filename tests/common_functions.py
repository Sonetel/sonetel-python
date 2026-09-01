import os

from sonetel import Auth
from sonetel import exceptions as e

_cached_token = None


def access_token():
    global _cached_token
    if _cached_token is not None:
        return _cached_token
    try:
        auth = Auth(
            username=os.getenv("SonetelUsername"), password=os.getenv("SonetelPassword")
        )
        _cached_token = auth.get_access_token()
        return _cached_token
    except e.AuthException as error:
        print(error)
        return None
