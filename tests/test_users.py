import os
import pytest
from uuid import uuid4
from sonetel import User
from sonetel import Auth
from sonetel import exceptions as e


def access_token():
    try:
        auth = Auth(username=os.getenv('SonetelUsername'), password=os.getenv('SonetelPassword'))
        return auth.get_access_token()
    except e.AuthException as error:
        print(error)
        return None


token = access_token()
if token:
    user = User(access_token=token)
else:
    raise e.AuthException('Cannot get access token')

def test_user_init():
    # Test if the user object is initialized
    assert user is not None

def test_user_failed():
    # Test if the user object initialization fails
    with pytest.raises(Exception) as e_info:
        User(access_token='eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJ1c2VyX2lkIjoiMjAwMDA0NjAwMCIsInVzZXJfbmFtZSI6InNhbV9kb2VAZXhhbXBsZS5jb20iLCJpc3MiOiJTb25ldGVsTm9kZTEyMyIsImV4cCI6IjE2ODQ0NzIxMDkiLCJpYXQiOiIxNjgxODgwMTA5IiwiYWNjX2lkIjoiMTIzNCIsImNsaWVudF9pZCI6InNvbmV0ZWwtd2ViIn0.ajVzgRfeLwB1IuMzldnzrmoUtUFFmh3QGmWQcs-3Flc')

def test_get_all_users():
    response = user.get(all_users=True)
    print(response['response'])
    assert response['status'] == 'success'

def test_get_invalid_user():
    user_invalid = user.get(userid='1234567890')
    assert user_invalid['status'] == 'success'
    assert user_invalid['response'] == None

def test_get_user():
    # Get a specific user
    response = user.get(userid=os.getenv('SonetelTestUserId'))
    assert response['response']['user_id'] == os.getenv('SonetelTestUserId')
    assert response['status'] == 'success'

def test_get_current_user():
    # Get current user
    response = user.get()
    assert response['status'] == 'success'
    assert response['response']['user_id'] == os.getenv('SonetelSelfUserId')
    assert response['response']['email'] == os.getenv('SonetelUsername')

def test_add_delete_user():

    # Add a new user
    email = f"{str(uuid4())}@example.com"
    password = str(uuid4())[:30]

    response_add = user.add(
        email=email,
        f_name='Test',
        l_name='User',
        user_type='regular',
        password=password
    )
    if response_add['status'] == 'failed':
        raise e.UserException(response_add['response']['detail'])
    assert response_add['status'] == 'success'
    user_to_delete = response_add['response']['user_id']
    assert response_add['response']['email'] == email
    assert response_add['response']['type'] == 'regular'

    # Delete the new user added
    response_del = user.delete(userid=user_to_delete)
    assert response_del['status'] == 'success'
    assert response_del['response'] == 'User deleted successfully'
