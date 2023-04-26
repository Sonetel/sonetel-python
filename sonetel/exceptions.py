class SonetelException(Exception):
    """
    General exception class.
    """
    def __init__(self, message):
        super().__init__(message)

class AuthException(SonetelException):
    """
    Authentication errors
    """
    pass

class AccountException(SonetelException):
    """
    Error related to the Sonetel account.
    """

class NumberException(SonetelException):
    """
    Phone number related error
    """
    pass

class VoiceAppException(SonetelException):
    """
    Errors related to voice apps
    """
    pass

class UserException(SonetelException):
    """
    Errors related to the User API
    """
    pass
