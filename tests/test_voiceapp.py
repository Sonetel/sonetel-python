import os
from uuid import uuid4

import pytest

from sonetel import VoiceApp
from sonetel import exceptions as e
from tests.common_functions import access_token

token = access_token()
if token:
    voice_app = VoiceApp(access_token=token)
else:
    raise e.AuthException("Cannot get access token")


def test_voice_app_init():
    # Test if the voice app object is initialized
    assert voice_app is not None


def test_voice_app_get():
    # Get all voice apps
    response = voice_app.get()
    assert response["status"] == "success"
