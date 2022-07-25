# Import Packages.
try:
    import requests
    import re
    from json import dumps
    import jwt
except ImportError as e:
    raise ImportError(e)

class Account:
    """
    Use Sonetel's Python module to manage your account.

    API documentation: https://docs.sonetel.com/

    """

    def __init__(self, username: str, password: str,
                 auth_url='https://api.sonetel.com/SonetelAuth/beta/oauth/token',
                 base_url='https://public-api.sonetel.com'):

        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError

        self.__username = username
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

    def get_token(self):
        return self._token if self._token else False

    def get_username(self):
        return self.__username if self.__username else False

    def get_userid(self):
        return self._userid if self._userid else False

    def get_accountid(self):
        return self._accountid if self._accountid else False

    def _decode_token(self):
        return jwt.decode(self._token, options={"verify_signature": False})

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

        if grant_type == 'refresh_token' and refresh_token is None:
            raise ValueError("A 'refresh_token' is needed.")

        # Prepare the request body.
        body = f"grant_type={grant_type}&username={self.__username}&password={self.__password}&refresh={refresh}"

        # Add the refresh token to the request body if passed to the function
        if refresh_token is not None and grant_type == 'refresh_token':
            body += f"&refresh_token={refresh_token}"

        auth = ('sonetel-api', 'sonetel-api')

        # Prepare the request headers
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Send the request
        r = requests.post(
            url=self._auth_url,
            data=body,
            headers=headers,
            auth=auth
        )

        # Check the response and handle accordingly.
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print(r.json())
            r.raise_for_status()

    def account_info(self):

        """
        Get information about Sonetel account such as the account ID, prepaid balance, currency, country, etc.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTUyNTkwNTM-get-your-account-information

        :return: A dict with the the Sonetel account details.
        """

        # Prepare the request Header
        header = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json"
        }

        # Send the request
        r = requests.get(
            url=f"{self._base_url}/account/{self._accountid}",
            headers=header)

        # Check the response and handle accordingly
        if r.status_code == requests.codes.ok:
            response = r.json()
            return response
        else:
            print(r.json())
            r.raise_for_status()

    def get_balance(self, currency: bool = False) -> str:
        """
        Get the prepaid account balance. Example, '3.74 USD' or '3.74'.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTUyNTkwNTM-get-your-account-information

        :param currency: Optional. Flag to specify if the currency should be returned or not. Defaults to False
        :return: The current prepaid balance.
        """

        # Prepare the request Header
        header = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json"
        }

        # Send the request
        r = requests.get(
            url=f"{self._base_url}/account/{self._accountid}",
            headers=header)

        # Check the response and handle accordingly
        if r.status_code == requests.codes.ok:
            response = r.json()
            if currency:
                return response['response']['credit_balance'] + ' ' + response['response']['currency']
            return response['response']['credit_balance']
        else:
            print(r.json())
            r.raise_for_status()

    # Fetch details of all users in account
    def account_users(self) -> list:
        """
        Get a list of all the users in the Sonetel account along with their settings
        such as title, email, password status, etc.
        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/b3A6MTY4MzEyMDQ-list-all-users

        :return: Returns a list containing the user information
        """

        # Prepare the request Header
        request_header = {
            "Authorization": "Bearer " + self._token
        }

        # Send the request
        r = requests.get(
            url=f'{self._base_url}/account/{self._accountid}/user/',
            headers=request_header
        )
        # Check the response and handle accordingly
        if r.status_code == requests.codes.ok:
            response = r.json()
            return response['response']
        else:
            print(r.json())
            r.raise_for_status()

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
                'Content-Type': 'application/json;charset=UTF-8'
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
                url=f'{self._base_url}/make-calls/call/call-back',
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
            "Content-Type": "application/json"
        }

        # Send the request
        r = requests.post(
            url=f'{self._base_url}/account/{self._accountid}/phonenumbersubscription/',
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

        # Prepare the request Header
        request_header = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json"
        }

        # Send the request
        r = requests.get(
            url=f'{self._base_url}/account/{self._accountid}/phonenumbersubscription/',
            headers=request_header
        )

        # Check the response and handle accordingly
        if r.status_code == requests.codes.ok:
            response = r.json()
            if response['response'] == 'No entries found':
                return ['No entries found']
            else:
                if 'e164only' in kwargs:
                    # Return only the E164 numbers if e164only = True
                    if kwargs['e164only']:
                        nums = []
                        for entry in response['response']:
                            nums.append(entry['phnum'])
                        return nums
                    else:
                        return response['response']
                return response['response']
        else:
            r.raise_for_status()
