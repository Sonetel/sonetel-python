"""
Users
"""
from json import dumps
from . import utilities as util
from . import _constants as const
from . import exceptions as e

class User(util.Resource):
    """
    Create and manage users in a Sonetel account
    """

    def __init__(self, access_token: str):
        if not access_token:
            raise e.AuthException('access_token is required')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_USER}'

    def get(self, all_users: bool = False, userid: str = ''):
        """
        Fetch details about all users or a specific user.

        If userid is not included with the request, details of the current user are fetched.

        :param all_users: Boolean. Optional. Get a list of all the users in the account. Defaults to False.
        :param userid: String. Optional. ID of a specific user to get the information for.
        """

        url = self._url

        if userid:
            url += userid
        elif not all_users:
            url += self._userid

        return util.send_api_request(
            token=self._token,
            uri=url,
            method='get') if util.is_valid_token(self._decoded_token) else False

    def add(self,
            email: str,
            f_name: str,
            l_name: str,
            password: str,
            user_type: str = 'regular'
            ) -> dict:
        """
        Adds a new user. Account admin privilege required.

        :param email: Required. String. The email address of the user.
        :param f_name: Required. String. The first name of the user
        :param l_name: Required. String. The last name of the user.
        :param password: Required. String. The password to be used.
        :param user_type: Required. String. The privilege level of the new user. Accepted values regular and admin.
        Defaults to regular.
        """

        # Checks
        if not password:
            return util.prepare_error(
                code=const.ERR_USER_DETAIL_EMPTY,
                message='password cannot be empty'
            )

        if not email:
            return util.prepare_error(
                code=const.ERR_USER_DETAIL_EMPTY,
                message='email cannot be empty'
            )

        if not f_name:
            return util.prepare_error(
                code=const.ERR_USER_DETAIL_EMPTY,
                message='first name cannot be empty'
            )

        if not l_name:
            return util.prepare_error(
                code=const.ERR_USER_DETAIL_EMPTY,
                message='last name cannot be empty'
            )

        # Request
        url = self._url
        body = {
            "user_fname": f_name,
            "user_lname": l_name,
            "email": email,
            "password": password,
            "type": user_type
        }

        return util.send_api_request(
            token=self._token,
            uri=url,
            method='post',
            body=dumps(body)
        )

    def delete(self, userid: str):
        """
        Delete a user from your Sonetel account.

        :param userid: String. Required. The unique ID of the user to be deleted.
        """
        if not userid:
            return util.prepare_error(
                code=const.ERR_USED_ID_EMPTY,
                message='user id cannot be empty'
            )

        url = self._url + userid

        return util.send_api_request(
            token=self._token,
            uri=url,
            method='delete'
            )

    def update(self, request: dict):
        """
        update user settings
        """
        raise NotImplementedError
