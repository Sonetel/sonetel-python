"""
Constants: API urls and other static data
"""

# General
API_URI_BASE = 'https://public-api.sonetel.com'
API_URI_AUTH = 'https://api.sonetel.com/SonetelAuth/beta/oauth/token'
API_AUDIENCE = 'api.sonetel.com'
PKG_VERSION = '0.2.1'

# Headers
CONTENT_TYPE_GENERAL = 'application/json;charset=UTF-8'
CONTENT_TYPE_AUTH = 'application/x-www-form-urlencoded'

# Authentication
CONST_JWT_USER = 'sonetel-api'
CONST_JWT_PASS = 'sonetel-api'
CONST_TYPES_GRANT = ['password', 'refresh_token']
CONST_TYPES_REFRESH = ['yes', 'no']

# API Resources
API_ENDPOINT_ACCOUNT = '/account/'
API_ENDPOINT_CALLBACK = '/make-calls/call/call-back'
API_ENDPOINT_NUMBERSUBSCRIPTION = '/phonenumbersubscription/'
API_ENDPOINT_VOICEAPP = '/voiceapp/'
API_ENDPOINT_USER = '/user/'
API_ENDPOINT_CALL_RECORDING = '/call-recording'

# Users
CONST_TYPES_USER = ['regular', 'admin']

# Phone Numbers
CONST_CONNECT_TO_TYPES = ['user', 'phnum', 'sip', 'app']

# Error codes
ERR_NUM_NOT_E164 = 1000
ERR_NUM_UPDATE_EMPTY = 1001
ERR_USER_DETAIL_EMPTY = 2000
ERR_USED_ID_EMPTY = 2001
ERR_ACCOUNT_UPDATE_BODY_EMPTY = 3000
ERR_CALLBACK_NUM_EMPTY = 4000

