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
        self._url = f'{const.API_URI_BASE}{const.API_ENDPOINT_CALL_RECORDING}?account_id={self._accountid}'

    def get(self, **kwargs):
        """
        Get a list of all the call recordings.

        - start_time: Timestamp. The start timestamp in the format YYYYMMDDTHH:MM:SSZ. Example 20201231T23:59:59. Limit
         the results to recordings created after this timestamp.
        - end_time: Timestamp. The end timestamp in the format YYYYMMDDTHH:MM:SSZ. Example 20221123T18:59:59. Limit the
         results to recordings created before this timestamp.
        - rec_id: String. The unique recording ID. If not included, returns all the recordings.
        - access_details: Boolean. Include the details needed to download recordings.
        - call_details: Boolean. Include the details of the voice calls.
        """

        url = self._url

        if len(kwargs) > 0:
            params = []
            fields = []
            try:
                if kwargs['access_details']:
                    fields.append('file_access_details')
            except KeyError:
                pass
            try:
                if kwargs['call_details']:
                    fields.append('voice_call_details')
            except KeyError:
                pass
            try:
                if kwargs['start_time']:
                    params.append(f'created_date_min={kwargs["start_time"]}')
            except KeyError:
                pass
            try:
                if kwargs['end_time']:
                    params.append(f'created_date_min={kwargs["end_time"]}')
            except KeyError:
                pass

            # Add fields and params to url.
            if len(fields) > 0:
                url += "fields=" + ",".join(fields)

            if len(params) > 0:
                for p in params:
                    url += p

        return util.send_api_request(token=self._token, uri=url, method='get')

    def delete(self, recording_id: str):
        """
        delete call recording
        """
        raise NotImplementedError
