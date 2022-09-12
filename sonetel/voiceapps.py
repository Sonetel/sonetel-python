import utilities as util
import constants as const

class VoiceApp(util.Resource):
    """
    Voice app calss.
    """
    def __init__(self, access_token):
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
