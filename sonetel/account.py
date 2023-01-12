"""
Manage your Sonetel account
"""
from json import dumps
from . import utilities as util
from . import constants as const
from . import exceptions as e

class Account(util.Resource):
    """
    Class representing the company account.
    """

    def __init__(self, access_token: str):
        if not access_token:
            raise e.AuthException('access_token missing')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}/{const.API_ENDPOINT_ACCOUNT}/{self._accountid}'

    def get(self) -> dict:
        """
        Information about your Sonetel account.

        :returns: The account information.
        """

        return util.send_api_request(
            token=self._token,
            uri=self._url,
            method='get',
        )

    def update(self, name: str = '', language: str = '', timezone: str = '') -> dict:
        """
        Update your account information. Pass one or more of the following parameters:

        :param name: String. New company name.
        :param language: String. The ID of the new language you want to switch to. Changes the language you see in app.sonetel.com
        :param timezone: String. The ID of the new timezone you want to switch to.

        :returns: The updated account information if the request was processed successfully.
        """

        body = {}
        if name:
            body['name'] = name
        if language:
            body['language'] = language
        if timezone:
            body['timezone_details'] = {
                "zone_id": timezone
            }
        if len(body) == 0:
            return util.prepare_error(
                code=const.ERR_ACCOUNT_UPDATE_BODY_EMPTY,
                message='request body cannot be empty'
            )

        return util.send_api_request(
            token=self._token,
            uri=self._url,
            method='put',
            body=dumps(body)
        )

    def get_balance(self, currency: bool = False) -> str:
        """
        Get the current prepaid balance in the account

        :param currency: Boolean. Optional. Set to true if currency should be returned in the response.
        :returns: A string representing the current prepaid balance in the Sonetel account.
        """

        response = util.send_api_request(
            token=self._token,
            uri=self._url,
            method='get',
        )

        balance = response['response']['credit_balance']
        if currency:
            balance += f" {response['response']['currency']}"

        return balance

    def get_accountid(self) -> str:
        """
        Get your account ID.

        :returns: String. Sonetel account ID.
        """
        return self._accountid
