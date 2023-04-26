"""
Add and manage phone numbers in your Sonetel account.
"""
import re
from json import dumps
from . import utilities as util
from . import _constants as const
from . import exceptions as e


def is_e164(number: str) -> bool:
    """
    Checks if a number is e164 formatted. Returns True if it is, False if it isn't.

    :param number: The number to check. For example, +441234567890.
    :return: True if the number is e164 formatted, False if it isn't.
    """
    if re.search(r'^\+?[1-9]\d{7,15}$', number):
        return True
    return False


class PhoneNumber(util.Resource):
    """
    Phone number class
    """

    def __init__(self, access_token):
        if not access_token:
            raise e.AuthException('access_token is required')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_ACCOUNT}{self._accountid}' \
                    f'{const.API_ENDPOINT_NUMBERSUBSCRIPTION}'

    def get(self, e164only: bool = True, number: str = '') -> dict:
        """
        List all the phone numbers present in the account.

        :param e164only: Optional. Boolean. Only return a list of phone numbers if set to True.
        Set to True by default.
        :param number: Optional. String. If you only want information about one of your numbers, pass it as a string.

        **DOCS**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE2MjQ3MzI4-phone-numbers

        :return: Information about the numbers assigned to account.
        """

        url = self._url

        if not isinstance(number, str):
            number = str(number)

        if number:
            if is_e164(number):
                url += number
            else:
                return util.prepare_error(
                    code=const.ERR_NUM_NOT_E164,
                    message=f'"{number}" is not a valid e164 number'
                )

        api_response = util.send_api_request(token=self._token, uri=url)
        response = api_response['response']

        # No numbers are found
        if response == 'No entries found':
            return {
                'status': 'success',
                'response': 'No entries found'
            }

        # Only return a list of e164 numbers, without any additional metadata
        if e164only:
            nums = []
            for entry in response:
                nums.append(entry['phnum'])
            return {
                'status': 'success',
                'response': nums
            }

        # Return full response
        return {
                'status': 'success',
                'response': response
            }

    def add(self, number: str) -> dict:
        """
        Buy a phone number that is available. Numbers that are available for purchase can be checked
        from the ``/availablephonenumber`` API endpoint.

        **DOCS**: https://docs.sonetel.com/docs/sonetel-documentation/YXBpOjE2MjQ3MzI4-phone-numbers

        :param number: the phone number you want to purchase.
        :return: Dict containing the success response or an error message.
        """
        if not isinstance(number, str):
            number = str(number)

        # Request body
        if is_e164(number):
            body = {
                "phnum": number
            }
        else:
            return util.prepare_error(
                code=const.ERR_NUM_NOT_E164,
                message=f'"{number}" is not a valid e164 number'
            )

        return util.send_api_request(
            token=self._token,
            uri=self._url,
            method='post',
            body=dumps(body)
        )

    def delete(self, number: str):
        """
        Remove a number from account. The phone number is removed immediately and cannot be recovered.

        :param number: The phone number to remove from account.
        :return: Dict containing the success response or an error message.
        """
        if not isinstance(number, str):
            number = str(number)

        if is_e164(number):
            url = f'{self._url}{number}'
        else:
            return util.prepare_error(
                code=const.ERR_NUM_NOT_E164,
                message=f'"{number}" is not a valid e164 number'
            )

        return util.send_api_request(
            token=self._token,
            uri=url,
            method='delete'
        )

    def update(self, number: str, connect_to_type: str, connect_to) -> dict:
        """
        Update the number's call forwarding settings.

        :param number: E164number for which the settings should be updated
        :param connect_to: the ID of the destination where the incoming calls to this number should be forwarded.
        :param connect_to_type: The destination type where the calls should be forwarded. Accepted values 'user', 'phnum', 'sip' and 'app'.
        """

        # Checks
        if not number:
            return util.prepare_error(
                code=const.ERR_NUM_UPDATE_EMPTY,
                message='number is required to update call settings'
            )
        if not connect_to:
            return util.prepare_error(
                code=const.ERR_NUM_UPDATE_EMPTY,
                message='connect_to is required to update call settings'
            )
        if connect_to_type not in const.CONST_CONNECT_TO_TYPES:
            return util.prepare_error(
                code=const.ERR_NUM_UPDATE_EMPTY,
                message=f'invalid connect_to_type value - {connect_to_type}'
            )

        # Prepare request
        body = {
            "connect_to_type": connect_to_type,
            "connect_to": connect_to
        }

        url = f'{self._url}{number}'

        # Return result
        return util.send_api_request(
            token=self._token,
            uri=url,
            method='put',
            body=dumps(body)
        )
