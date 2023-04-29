"""
Make Phone Calls
"""
# Import Packages.
from json import dumps
from . import utilities as util
from . import _constants as const
from . import exceptions as e

class Call(util.Resource):
    """Initiate callback calls using Sonetel's CallBack API.

    :param access_token: Required. The access token generated from the Auth class.
    :param app_name: Optional. The name of the app that is making the request. Defaults to 'PythonSonetelPackage'. This is used to identify the app in logs.

    :return: Return the status code and message as a dict. For example, `{'code': 200, 'message': 'OK'}`
    """

    def __init__(self, access_token, app_name: str = 'PythonSonetelPackage') -> None:
        if not access_token:
            raise e.AuthException('access_token is required')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_CALLBACK}'

        if len(app_name) < 2:
            raise e.SonetelException('app_name must be at least 2 characters long')
        
        self._app_name = f"{app_name}__{self._accountid}__{self._userid}"

    def callback(self, num1: str, num2: str, cli1: str = 'automatic', cli2: str = 'automatic'):
        """
        Use Sonetel's CallBack API to make business quality international calls at the cost of 2 local calls.

        :param num1: Required. The first phone number that will be called. This should be your phone number, SIP address or Sonetel email address.
        :param num2: Required.The phone number or address that you wish to connect to.
        :param cli1: Optional. The caller ID shown to the first person. Defaults to automatic.
        :param cli2: Optional. The caller ID shown to the second person. Defaults to automatic.

        :return: Return the status code and message as a dict.

        **Docs**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE1OTMzOTIy-make-calls

        **Number Format:**\n
        It is recommended that both the phone numbers (num1 and num2) be entered in the international E164 format with a
        leading +. For example, if you want to call a US number (212) 555-1234, it should be set as `+12125551234`.

        However you can also provide SIP addresses. Additionally, `num1` can be your Sonetel username - this will make
        sure that the incoming call to you is handled as per your incoming settings defined in the app.

        **Caller ID:**\n
        It is best to use 'automatic' CLI as our system selects the best possible phone to be shown from the numbers
        available in your account. If you don't have a Sonetel number, then your verified mobile number is used as CLI.
        Read more at https://sonetel.com/cli

        """

        # Check if num1 and num2 are defined.
        if num1 and num2:

            # Initiate the callback
            body = {
                "app_id": f'{self._app_name}-{const.PKG_VERSION}',
                "call1": num1,
                "call2": num2,
                "show_1": cli1,
                "show_2": cli2
            }

            return util.send_api_request(
                token=self._token,
                uri=self._url,
                method='post',
                body=dumps(body)
            )
        return util.prepare_error(
            code=const.ERR_CALLBACK_NUM_EMPTY,
            message='num1 & num2 are required to make a call.'
        )
