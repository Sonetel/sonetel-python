"""
Voice apps
"""
from . import utilities as util
from . import _constants as const
from . import exceptions as e


class VoiceApp(util.Resource):
    """
    Voice app class.
    """

    def __init__(self, access_token):
        if not access_token:
            raise e.AuthException("access_token is required")

        super().__init__(access_token=access_token)
        self._url = f"{const.API_URI_BASE}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_VOICEAPP}"

    def get(self, app_id: str = None):
        """
        Get voice apps. Specify the app_id to get a specific voice app or leave it blank to get all voice apps in the Sonetel account.

        :param app_id: Optional. The ID of the voice app to get. Defaults to None.
        """
        if app_id:
            self._url = f"{self._url}/{app_id}"

        return util.send_api_request(token=self._token, uri=self._url)
