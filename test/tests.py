"""
Basic Tests
"""

import os
import sonetel

# Set the username and password
user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')

if not user or not pswd:
    raise Exception('Cannot fetch username or password from environment variables.')

def test_auth( user_name, password, count):
    """
    test
    """
    sntl = sonetel.Auth(username = user_name, password=password)
    access_token = sntl.get_access_token()
    test_string = access_token.split('.')

    try:
        print(f"Test {count}")
        assert test_string[0] == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9'
    except AssertionError as assert_error:
        print(f'\tFail. {str(assert_error)}')
    else:
        print('\tOK')
    return access_token

def test_account(access_token):
    """
    Test the Account resource
    """
    a = sonetel.Account(access_token)

    tests = [
        {
            'name': 'account_id',
            'test': a.get_accountid(),
            'return_type': int
        },
        {
            'name': 'get_balance',
            'test': a.get_balance(),
            'return_type': str
        },
        {
            'name': 'get_balance_currency',
            'test': a.get_balance(currency=True),
            'return_type': str
        },
        {
            'name': 'get_account',
            'test': a.get(),
            'return_type': dict
        }
    ]

    for test in tests:
        if isinstance(test['test'],test['return_type']):
            print(f'\t\t Success {test["name"]} - {test["test"]}')
        else:
            print(f'\t\t Failed {test["name"]}')

def test_voice_app(access_token):
    """
    Test the VoiceApp resource
    """
    # To be implemented
    assert True is True

def run_test(test_name,access_token,test_count):
    """
    Run tests using the function passed
    """
    try:
        print(f"Test {test_count} - {test_name.__name__}")
        test_name(access_token)
    except AssertionError as assert_error:
        print(f'\tFail. {str(assert_error)}')
    else:
        print('\tOK')
    finally:
        test_count += 1

    return test_count

if __name__ == '__main__':
    TEST_COUNT = 1
    token = test_auth(user_name=user, password=pswd, count=TEST_COUNT)
    TEST_COUNT += 1
    run_test(test_account,token,TEST_COUNT)
    run_test(test_voice_app,token,TEST_COUNT)

    print(f'{TEST_COUNT - 1} tests passed')
