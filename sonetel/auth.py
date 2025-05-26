"""
# Auth

The Auth class is used to manage handle authentication with the Sonetel system. It can be used to create, refresh and fetch tokens.

It contains the following methods:

* `create_token()` - Create an API access token from the user's Sonetel email address and password.
* `get_access_token()` - Get the access token.
* `get_decoded_token()` - Get the decoded access token.
* `get_refresh_token()` - Get the refresh token.

"""

import requests

# Import Packages.
from jwt import decode

from . import _constants as const
from . import exceptions as e
from . import utilities as util


class Auth:
    """
    Authentication class. Create, refresh and fetch tokens.
    """

    def __init__(self, username: str, password: str):

        self.__username = username
        self.__password = password

        # Get access token from API
        token = self.create_token()
        self._access_token = token["access_token"]
        self._refresh_token = token["refresh_token"]
        self._decoded_token = decode(
            self._access_token,
            audience="api.sonetel.com",
            options={"verify_signature": False},
        )

    def create_token(
        self,
        refresh_token: str = "",
        grant_type: str = "password",
        refresh: str = "yes",
    ):
        """
        Create an API access token from the user's Sonetel email address and password.
        Optionally, generate a refresh token. Set the ``grant_type`` to ``refresh_token`` to refresh an
        existing access token.

        **Documentation**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjExMzI3NDM3-authentication

        Args:
            refresh: Optional. Flag to return refresh token in the response. Accepted values 'yes' and 'no'. Defaults to 'yes'
            grant_type: Optional. The OAuth2 grant type - `password` and `refresh_token` accepted. Defaults to 'password'
            refresh_token: Optional. Pass the `refresh_token` generated from a previous request in this field to generate a new access_token.

        Returns:
            dict: The access token and refresh token if the request was processed successfully. If the request failed, the error message is returned.
        """

        # Checks
        if grant_type.strip().lower() not in const.CONST_TYPES_GRANT:
            raise e.AuthException(f"invalid grant: {grant_type}")

        if refresh.strip().lower() not in const.CONST_TYPES_REFRESH:
            refresh = "yes"

        if grant_type.strip().lower() == "refresh_token" and not refresh_token:
            refresh_token = self._refresh_token

        # Prepare the request body.
        body = f"grant_type={grant_type}&refresh={refresh}"

        # Add the refresh token to the request body if passed to the function
        if grant_type == "refresh_token":
            body += f"&refresh_token={refresh_token}"
        else:
            body += f"&username={self.__username}&password={self.__password}"

        # Prepare the request
        auth = (const.CONST_JWT_USER, const.CONST_JWT_PASS)

        # Use session manager for the request
        session = util.get_session()
        response = session.request(
            method="post",
            url=const.API_URI_AUTH,
            body=body,
            content_type=const.CONTENT_TYPE_AUTH,
            auth=auth,
        )

        # Check for success and handle token updates
        if response.get("status") != "failed" and "access_token" in response:
            if refresh_token and grant_type == "refresh_token":
                self._access_token = response["access_token"]
                self._refresh_token = response["refresh_token"]
                self._decoded_token = decode(
                    self._access_token,
                    audience="api.sonetel.com",
                    options={"verify_signature": False},
                )
            return response

        return response  # This will contain error details if it failed

    def get_access_token(self):
        """
        Returns the access token.

        Examples:
            >>> from sonetel import Auth
            >>> auth = Auth('username', 'password')
            >>> auth.get_access_token()
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhcGkuc29uZXRlbC5jb20iLCJleHAiOjE2MjQwNjY0NzgsImlhdCI6MTYyNDA2Mzg3OCwiaXNzIjoic29uZXRlbC5jb20iLCJqdGkiOiIyMjIyMjIiLCJzdWIiOiJzb25l'

        Args:
            None

        Returns:
            access_token (str): The access token that can be used to access other account resources.
        """
        return self._access_token if hasattr(self, "_access_token") else False

    def get_refresh_token(self):
        """
        Return the refresh token that can be exchanged for a new access token.

        Examples:
            >>> from sonetel import Auth
            >>> auth = Auth('username', 'password')
            >>> auth.get_refresh_token()
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhcGkuc29uZXRlbC5jb20iLCJleHAiOjE2MjQwNjY0NzgsImlhdCI6MTYyNDA2Mzg3OCwiaXNzIjoic29uZXRlbC5jb20iLCJqdGkiOiIyMjIyMjIiLCJzdWIiOiJzb25l'

        Args:
            None

        Returns:
            str: The refresh token.
        """
        return self._refresh_token if hasattr(self, "_refresh_token") else False

    def get_decoded_token(self):
        """
        Decodes the access token and returns the decoded token.

        > Note: This method only decodes the payload - it does not verify the signature.

        Examples:
            >>> from sonetel import Auth
            >>> auth = Auth('username', 'password')
            >>> auth.get_decoded_token()
            {'aud': 'api.sonetel.com', 'exp': 1624066478, 'iat': 1624063878, 'iss': 'sonetel.com', 'jti': '222222', 'sub': 'sonetel'}

        Args:
            None

        Returns:
            dict: The decoded token.
        """
        return self._decoded_token if hasattr(self, "_decoded_token") else False
