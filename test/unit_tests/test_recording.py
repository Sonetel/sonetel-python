import os
from sonetel import Auth
from sonetel import Recording
from sonetel import exceptions as e

def access_token():
    try:
        auth = Auth(username=os.getenv('SonetelUsername'), password=os.getenv('SonetelPassword'))
        return auth.get_access_token()
    except e.AuthException as error:
        raise e.AuthException(f"Error: {error}")


token = access_token()

def test_recording_get_all():
    recording = Recording(access_token=token)
    result = recording.get()

    assert result['status'] == 'success'
    assert type(result['response']) == list

def test_recording_get_single():
    recording = Recording(access_token=token)
    result = recording.get(rec_id='REd2jiyro9azqj')

    assert result['status'] == 'success'
    assert type(result['response']) == dict
    assert result['response']['call_recording_id'] == 'REd2jiyro9azqj'
    assert result['response']['account_id'] == 5033728

def test_recording_get_single_invalid_id():
    recording = Recording(access_token=token)
    result = recording.get(rec_id='invalid_id')

    assert result['status'] == 'failed'
    assert result['response']['detail'] == 'Invalid recording id'
