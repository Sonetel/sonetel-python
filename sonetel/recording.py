"""
Manage call recordings
"""
# Import Packages.
from . import utilities as util
from . import constants as const

class Recording(util.Resource):
    """
    Class representing the call recording resource.
    """

    def __init__(self, access_token: str = None):
        super().__init__(access_token)
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_CALL_RECORDING}'

    def get(self,
            start_time: str = None,
            end_time: str = None,
            file_access_details: bool = False,
            voice_call_details: bool = False,
            rec_id: str = None
            ):
        """
        Get a list of all the call recordings.

        :param start_time: The start timestamp in the format YYYYMMDDTHH:MM:SSZ. Example 20201231T23:59:59. Limit the results to recordings created after this timestamp.
        :param end_time: The end timestamp in the format YYYYMMDDTHH:MM:SSZ. Example 20221123T18:59:59. Limit the results to recordings created before this timestamp.
        :param rec_id: The unique recording ID. If not included, returns all the recordings.
        :param file_access_details: Boolean. Include the details needed to download recordings.
        :param voice_call_details: Boolean. Include the details of the voice calls.
        """

        url = self._url

        # Prepare the request URL based on the params passed to the method
        if rec_id:
            # Get a single recording
            url += f'/{rec_id}'
        else:
            # Search for and return multiple recordings
            url += f'?account_id={self._accountid}'

            if util.is_valid_date(start_time) and util.is_valid_date(end_time) and util.date_diff(start_time, end_time):
                url += f'&created_date_max={end_time}&created_date_min={start_time}'

            fields = []

            if file_access_details:
                fields.append('file_access_details')
            if voice_call_details:
                fields.append('voice_call_details')

            if len(fields) > 0:
                url += '&fields=' + ','.join(fields)

        return util.send_api_request(token=self._token, uri=url, method='get')

    def delete(self, recording_id: str):
        """
        delete call recording
        """
        raise NotImplementedError
