"""
Voice apps
"""
from . import utilities as util
from . import _constants as const
from . import exceptions as e

class VoiceApp(util.Resource):
    """
    Voice app calss.
    """
    def __init__(self, access_token):
        if not access_token:
            e.AuthException('access_token is required')

        super().__init__(access_token=access_token)
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_ACCOUNT}{self._accountid}{const.API_ENDPOINT_VOICEAPP}'

    def get(self):
        """
        Get voice apps
        """
        return util.send_api_request(
            token=self._token,
            uri=self._url
        )

    def add(self, voice_app_name: str, voice_app_type: str):
        """
        add a new voice app
        """
        raise NotImplementedError

    def update(self, voice_app_id: str):
        """
        Update a voice app
        """
        raise NotImplementedError

    def delete(self, voice_app_id: str):
        """
        delete existing voice app
        """
        raise NotImplementedError
