"""
Run tests on the Auth class
"""
import os
import sonetel as sntl

auth = sntl.Auth(username=os.getenv('SonetelUsername'), password=os.getenv('SonetelPassword'))

def test_get_access_token():
    access_token = auth.get_access_token()
    assert access_token is not None
    assert isinstance(access_token, str)
    assert access_token[:15] == 'eyJhbGciOiJSUzI'

def test_get_refresh_token():
    refresh_token = auth.get_refresh_token()
    assert refresh_token is not None
    assert isinstance(refresh_token, str)
    assert refresh_token[:15] == 'eyJhbGciOiJSUzI'

def test_get_decoded_token():
    decoded_token = auth.get_decoded_token()
    assert decoded_token is not None
    assert isinstance(decoded_token, dict)
    assert decoded_token['iss'] == 'SonetelNode123'
    assert decoded_token['aud'] == 'api.sonetel.com'
    assert 'user.read' in decoded_token['scope']
    assert 'user.write' in decoded_token['scope']

def test_refresh_token():
    refresh_token = auth.get_refresh_token()
    auth.create_token(refresh='yes', grant_type='refresh_token', refresh_token=refresh_token)
    access_token = auth.get_access_token()
    refresh_token = auth.get_refresh_token()
    assert auth.get_access_token() is not None
    assert auth.get_refresh_token() is not None
    assert auth.get_decoded_token() is not None
    assert isinstance(access_token, str)
    assert access_token[:15] == 'eyJhbGciOiJSUzI'
    assert refresh_token is not None
    assert isinstance(refresh_token, str)
    assert refresh_token[:15] == 'eyJhbGciOiJSUzI'
