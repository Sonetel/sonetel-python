# Import Packages.
import requests
from json import dumps
import jwt
from . import constants as const
from . import utilities

class API:
    """
    Use Sonetel's Python module to manage your account.

    API documentation: https://docs.sonetel.com/

    """

    def __init__(self, username: str, password: str,
                 auth_url=const.API_URI_AUTH,
                 base_url=const.API_URI_BASE):

        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError

        self._username = username
        self.__password = password

        # API URLs
        self._auth_url = auth_url
        self._base_url = base_url

        # Set the API access token
        token = self.create_token()
        self._token = token["access_token"]
        self._refresh_token = token["refresh_token"]
        self._decoded_token = self._decode_token()

        # Account and User Information
        self._accountid = self._decoded_token['acc_id']
        self._userid = self._decoded_token['user_id']

    def __str__(self):
        return str({
            "username": self._username,
            "accountid": self._accountid,
            "prepaid_balance": self.get_balance(currency=True),
            "phone_numbers": self.subscription_listnums(e164only=True),
            "details": self.account_info()
        })

    def _send_api_request(self, uri: str):

        # Prepare the request Header
        request_header = {
            "Authorization": "Bearer " + self._token
        }

        # Send the request
        r = requests.get(
            url=uri,
            headers=request_header
        )

        if r.status_code == requests.codes.ok:
            response = r.json()
            return response
        else:
            print(r.json())
            r.raise_for_status()

    def get_token(self):
        return self._token if hasattr(self, "_token") else False

    def get_decodedtoken(self):
        return self._decoded_token if hasattr(self, "_decoded_token") else False

    def get_refreshtoken(self):
        return self._refresh_token if hasattr(self, "_refresh_token") else False

    def get_username(self):
        return self._username if hasattr(self, "_username") else False

    def get_userid(self):
        return self._userid if hasattr(self, "_userid") else False

    def get_accountid(self):
        return self._accountid if hasattr(self, "_accountid") else False

    def _decode_token(self):
        return jwt.decode(
            self._token,
            audience=const.API_AUDIENCE,
            options={"verify_signature": False}
            )

    def create_token(self, refresh: str = "yes", grant_type: str = "password", refresh_token: str = None) -> dict:
        """
        Create an API access token from the user's Sonetel email address and password.
        Optionally, generate a refresh token as well. Set the ``grant_type`` to ``refresh_token`` to refresh an
        existing access token.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjExMzI3NDM3-authentication

        :param refresh: Optional. Flag to control whether a refresh token is included in the response. Defaults to 'yes'
        :param grant_type: Optional. The OAuth2 grant type. Defaults to 'password'
        :param refresh_token: Optional. Pass the `refresh_token` in this field to generate a new access_token.

        :return: Returns the access token.
        """

        try:
            refresh_token = self._refresh_token
        except AttributeError:
            pass

        if grant_type == 'refresh_token' and refresh_token is None:
            raise ValueError("A 'refresh_token' is needed.")

        # Prepare the request body.
        body = f"grant_type={grant_type}&refresh={refresh}"

        # Add the refresh token to the request body if passed to the function
        if refresh_token is not None and grant_type == 'refresh_token':
            body += f"&refresh_token={refresh_token}"
        else:
            body += f"&username={self._username}&password={self.__password}"

        auth = (const.CONST_JWT_USER, const.CONST_JWT_PASS)

        # Prepare the request headers
        headers = {'Content-Type': const.CONTENT_TYPE_AUTH}

        # Send the request
        r = requests.post(
            url=self._auth_url,
            data=body,
            headers=headers,
            auth=auth
        )

        # Check the response and handle accordingly.
        if r.status_code == requests.codes.ok:
            response_json = r.json()

            if refresh_token is not None and grant_type == 'refresh_token':
                self._token = response_json["access_token"]
                self._refresh_token = response_json["refresh_token"]

            return response_json
        else:
            print(r.json())
            r.raise_for_status()

    def account_info(self) -> dict:

        """
        Get information about Sonetel account such as the account ID, prepaid balance, currency, country, etc.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTUyNTkwNTM-get-your-account-information

        :return: A dict with the the Sonetel account details.
        """

        url = f"{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}"
        api_response = utilities.send_api_request(token=self._token, uri=url)
        return api_response['response']

    def get_balance(self, currency: bool = False) -> str:
        """
        Get the prepaid account balance. Example, '3.74 USD' or '3.74'.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTUyNTkwNTM-get-your-account-information

        :param currency: Optional. Flag to specify if the currency should be returned or not. Defaults to False
        :return: The current prepaid balance.
        """

        url = f"{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}"
        api_response = utilities.send_api_request(token=self._token, uri=url)
        balance = api_response['response']['credit_balance']

        if currency:
            return f"{balance}  {api_response['response']['currency']}"

        return balance

    # Fetch details of all users in account
    def account_users(self) -> list:
        """
        Get a list of all the users in the Sonetel account along with their settings
        such as title, email, password status, etc.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTY4MzEyMDQ-list-all-users

        :return: Returns a list containing the user information
        """
        url = f'{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_USER}'
        api_response = self.utilities.send_api_request(token=self._token, uri=url)
        return api_response['response']

    # Fetch a list of all the voice apps in the account
    def get_voiceapps(self) -> list:
        """
        Get a list of all the voice apps in the Sonetel account along with their settings
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTY4MzExODg-get-all-voice-apps

        :return: Returns a list containing the voice app information
        """

        url = f'{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_VOICEAPP}'
        api_response = self.utilities.send_api_request(token=self._token, uri=url)
        return api_response['response']

    def callback(self, num1: str, num2: str, cli1: str = 'automatic', cli2: str = 'automatic'):
        """
        Use Sonetel's CallBack API to make business quality international calls at the cost of 2 local calls.

        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE1OTMzOTIy-make-calls

        **Number Format:**\n
        It is recommended that both the phone numbers (num1 and num2) be entered in the international E164 format with a
        leading +. For example, if you want to call a US number (212) 555-1234, it should be set as `+12125551234`.

        However you can also provide SIP addresses. Additionally, `num1` can be your Sonetel username - this will make
        sure that the incoming call to you is handled as per your incoming settings defined in the app.

        **Caller ID:**\n
        It is best to use 'automatic' CLI as our system selects the best possible phone to be shown from the numbers
        available in your account. If you don't have a Sonetel number, then your verified mobile number is used as CLI.

        :param num1: Required. The first phone number that will be called.
        This should be your phone number, SIP address or Sonetel email address.
        :param num2: Required.The phone number that you wish to speak to.
        :param cli1: Optional. The caller ID shown to the first person. Defaults to automatic.
        :param cli2: Optional. The caller ID shown to the second person. Defaults to automatic.

        :return: Return the status code and message as a dict.
        """

        # Check if num1 and num2 are defined.
        if num1 and num1:
            # ToDo:
            #  1. Check cost of call before connecting
            #  2. Get list of numbers that can be used as caller ID.

            # Initiate the callback
            request_header = {
                'Authorization': 'Bearer ' + self._token,
                'Content-Type': const.CONTENT_TYPE_GENERAL
            }

            body = {
                "app_id": 'PythonSonetelApp-' + str(self._accountid),
                "call1": num1,
                "call2": num2,
                "show_1": cli1,
                "show_2": cli2
            }

            # Send the request
            r = requests.post(
                url=f'{self._base_url}{const.API_ENDPOINT_CALLBACK}',
                data=dumps(body),
                headers=request_header
            )

            # Check the response and handle accordingly
            if r.status_code == requests.codes.ok:
                response = r.json()
                return response['response']
            else:
                print(r.json())
                r.raise_for_status()
        else:
            raise ValueError('num1 & num2 are mandatory.')

    # Create a phone number subscription
    def subscription_buynum(self, number: str) -> dict:
        """
        Buy a phone number that is available. Numbers that are available for purchase can be checked
        from the ``/availablephonenumber`` API endpoint.

        **DOCS**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE2MjQ3MzI4-phone-numbers

        :param number: the phone number you want to purchase.
        :return: Dict containing the response in case of success.
        """

        # Prepare the request body
        body = {
            "phnum": number
        }

        # Prepare the request Header
        request_header = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": const.CONTENT_TYPE_GENERAL
        }

        # Send the request
        r = requests.post(
            url=f'{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_NUMBERSUBSCRIPTION}',
            data=dumps(body),
            headers=request_header
        )

        # Check the response and handle accordingly
        if r.status_code == requests.codes.ok:
            response = r.json()
            return response['response']
        else:
            r.raise_for_status()

    def subscription_listnums(self, **kwargs) -> list:
        """
        List all the phone numbers present in the account.

        - ``e164only``. Boolean. Only return a list of phone numbers is set to true

        **DOCS**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE2MjQ3MzI4-phone-numbers


        :return: Returns a list containing the information about the numbers assigned to you.
        """

        url = f'{self._base_url}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_NUMBERSUBSCRIPTION}'
        api_response = utilities.send_api_request(token=self._token, uri=url)
        response = api_response['response']

        if 'e164only' in kwargs:
            # Return only the E164 numbers if e164only = True
            if kwargs['e164only']:
                nums = []
                for entry in response:
                    nums.append(entry['phnum'])
                return nums

        # Check the response and handle accordingly
        if response == 'No entries found':
            return ['No entries found']

        return response
