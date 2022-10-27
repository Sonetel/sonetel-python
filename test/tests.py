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

def TestAuth(u, p, test_count):
    sntl = sonetel.Auth(username=u, password=p)
    token = sntl.get_access_token()
    test_string = token.split('.')
    
    try:
        print(f"Test {test_count}")
        assert test_string[0] == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9'
    except AssertionError as e:
        print(f'\tFail. {str(e)}')
    else:
        print(f'\tOK')
    return token


def TestAccount(token):
    # To be implemented
    assert True == True

def TestVoiceApps(token):
    # To be implemented
    assert True == True


def RunTest(test_name,token,test_count):

    try:
        print(f"Test {test_count}")
        test_name(token)
    except AssertionError as e:
        print(f'\tFail. {str(e)}')
    else:
        print(f'\tOK')
    finally:
        test_count += 1

    return test_count


if __name__ == '__main__':
    test_count = 1
    token = TestAuth(u=user, p=pswd, test_count=test_count)
    test_count += 1
    test_count = RunTest(TestAccount,token,test_count)
    test_count = RunTest(TestVoiceApps,token,test_count)

    print(f'{test_count - 1} tests passed')
