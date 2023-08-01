"""
# Account

The Account class is used to manage your Sonetel account information. You can use it to get information about your account such as the current prepaid balance, the account ID, and more.

You can also update your account information such as the company name, language, and timezone.

The class contains the following methods:

* `get()` - Get information about the Sonetel account.
* `update()` - Update your account information.
* `get_balance()` - Get the current prepaid balance in the account.
* `get_accountid()` - Get your account ID.

"""
from json import dumps
from . import utilities as util
from . import _constants as const
from . import exceptions as e

class Account(util.Resource):
    def __init__(self, access_token: str):
        if not access_token:
            raise e.AuthException('access_token missing')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}/{const.API_ENDPOINT_ACCOUNT}/{self._accountid}'

    def get(self) -> dict:
        """
        Get information about the Sonetel account.

        Examples:
            >>> account = Account(access_token='your_access_token')
            >>> acc_info = account.get()
            >>> print(acc_info['response']['name'])
            'ACME Inc.'
            >>> print(acc_info['response']['currency'])
            'USD'
        
        Args:
            None

        Returns:
            dict: The account information if the request was processed successfully.
        """

        return util.send_api_request(
            token=self._token,
            uri=self._url,
            method='get',
        )

    def update(self, name: str = '', language: str = '', timezone: str = '') -> dict:
        """
        Update your account information. Pass one or more of the following parameters:

        Examples:
            >>> account = Account(access_token='your_access_token')
            >>> acc_info = account.update(name='ACME Inc.', language='en', timezone='Europe/Stockholm')
            >>> print(acc_info['response']['name'])
            'ACME Inc.'

        Args:
            name (str): New company name.
            language (str): The ID of the new language you want to switch to. Changes the language you see in app.sonetel.com
            timezone (str): The ID of the new timezone you want to switch to.

        Returns:
            dict: The updated account information if the request was processed successfully.

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

        Examples:
            >>> account = Account(access_token='your_access_token')
            >>> print(account.get_balance())
            '1.23'
            >>> print(account.get_balance(currency=True))
            '1.23 USD'
        
        Args:
            currency (bool): Optional. Set to true if currency should be returned in the response.

        Returns:
            str: A string representing the current prepaid balance in the Sonetel account.

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
        Get your account ID. The account ID is used to uniquely identify your Sonetel account.

        Examples:
            >>> account = Account(access_token='your_access_token')
            >>> print(account.get_accountid())
            '123456789'

        Args:
            None

        Returns:
            str: The account ID.
        """
        return self._accountid
