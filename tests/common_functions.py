import os

from sonetel import Auth
from sonetel import exceptions as e


def access_token():
    try:
        auth = Auth(
            username=os.getenv("SonetelUsername"), password=os.getenv("SonetelPassword")
        )
        return auth.get_access_token()
    except e.AuthException as error:
        print(error)
        return None
