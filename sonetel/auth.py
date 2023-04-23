# Import Packages.
from jwt import decode
import requests
from . import _constants as const
from . import exceptions as e

class Auth:
    """
    Authentication class. Create, refresh and fetch tokens.
    """
    def __init__(self, username: str, password: str):

        self.__username = username
        self.__password = password

        # Get access token from API
        token = self.create_token()
        self._access_token = token['access_token']
        self._refresh_token = token['refresh_token']
        self._decoded_token = decode(
            self._access_token,
            audience='api.sonetel.com',
            options={"verify_signature": False}
        )

    def create_token(self,
                     refresh_token: str = '',
                     grant_type: str = 'password',
                     refresh: str = 'yes',
                     ):
        """
        Create an API access token from the user's Sonetel email address and password.
        Optionally, generate a refresh token. Set the ``grant_type`` to ``refresh_token`` to refresh an
        existing access token.

        **Documentation**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjExMzI3NDM3-authentication

        :param refresh: Optional. Flag to return refresh token in the response. Accepted values 'yes' and 'no'. Defaults to 'yes'
        :param grant_type: Optional. The OAuth2 grant type - `password` and `refresh_token` accepted. Defaults to 'password'
        :param refresh_token: Optional. Pass the `refresh_token` generated from a previous request in this field to generate a new access_token.

        :return: dict. The access token and refresh token if the request was processed successfully. If the request failed, the error message is returned.
        """

        # Checks
        if grant_type.strip().lower() not in const.CONST_TYPES_GRANT:
            raise e.AuthException(f'invalid grant: {grant_type}')

        if refresh.strip().lower() not in const.CONST_TYPES_REFRESH:
            refresh = 'yes'

        if grant_type.strip().lower() == 'refresh_token' and not refresh_token:
            refresh_token = self._refresh_token

        # Prepare the request body.
        body = f"grant_type={grant_type}&refresh={refresh}"

        # Add the refresh token to the request body if passed to the function
        if grant_type == 'refresh_token':
            body += f"&refresh_token={refresh_token}"
        else:
            body += f"&username={self.__username}&password={self.__password}"

        # Prepare the request
        auth = (const.CONST_JWT_USER, const.CONST_JWT_PASS)
        headers = {'Content-Type': const.CONTENT_TYPE_AUTH}

        # Send the request
        try:
            req = requests.post(
                url=const.API_URI_AUTH,
                data=body,
                headers=headers,
                auth=auth,
                timeout=60
            )
            req.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            return {'status': 'failed', 'error': 'ConnectionError', 'message': err}
        except requests.exceptions.Timeout:
            return {'status': 'failed', 'error': 'Timeout', 'message': 'Operation timed out. Please try again.'}
        except requests.exceptions.HTTPError as err:
            return {'status': 'failed', 'error': 'Timeout', 'message': err}

        # Check the response and handle accordingly.
        if req.status_code == requests.codes.ok: # pylint: disable=no-member
            response_json = req.json()

            if refresh_token and grant_type == 'refresh_token':
                self._access_token = response_json["access_token"]
                self._refresh_token = response_json["refresh_token"]
                self._decoded_token = decode(
                    self._access_token,
                    audience='api.sonetel.com',
                    options={"verify_signature": False}
                )

            return response_json
        return {'status': 'failed', 'error': 'Unknown error', 'message': req.text}

    def get_access_token(self):
        """
        Returns the access token
        """
        return self._access_token if hasattr(self, '_access_token') else False

    def get_refresh_token(self):
        """
        Return the refresh token
        """
        return self._refresh_token if hasattr(self, '_refresh_token') else False

    def get_decoded_token(self):
        """
        Returns the decoded token
        """
        return self._decoded_token if hasattr(self, '_decoded_token') else False
