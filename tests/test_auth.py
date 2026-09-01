"""
Run tests on the Auth class
"""

import http.server
import os
import threading
from unittest.mock import patch

import pytest

import sonetel as sntl
from sonetel import exceptions as e

auth = sntl.Auth(
    username=os.getenv("SonetelUsername"), password=os.getenv("SonetelPassword")
)


def test_get_access_token():
    access_token = auth.get_access_token()
    assert access_token is not None
    assert isinstance(access_token, str)
    assert access_token[:15] == "eyJhbGciOiJSUzI"


def test_get_refresh_token():
    refresh_token = auth.get_refresh_token()
    assert refresh_token is not None
    assert isinstance(refresh_token, str)
    assert refresh_token[:15] == "eyJhbGciOiJSUzI"


def test_get_decoded_token():
    decoded_token = auth.get_decoded_token()
    assert decoded_token is not None
    assert isinstance(decoded_token, dict)
    assert decoded_token["iss"] == "SonetelNode123"
    assert decoded_token["aud"] == "api.sonetel.com"
    assert "user.read" in decoded_token["scope"]
    assert "user.write" in decoded_token["scope"]


def test_refresh_token():
    refresh_token = auth.get_refresh_token()
    auth.create_token(
        refresh="yes", grant_type="refresh_token", refresh_token=refresh_token
    )
    access_token = auth.get_access_token()
    refresh_token = auth.get_refresh_token()
    assert auth.get_access_token() is not None
    assert auth.get_refresh_token() is not None
    assert auth.get_decoded_token() is not None
    assert isinstance(access_token, str)
    assert access_token[:15] == "eyJhbGciOiJSUzI"
    assert refresh_token is not None
    assert isinstance(refresh_token, str)
    assert refresh_token[:15] == "eyJhbGciOiJSUzI"


def test_create_token_invalid_grant_type():
    with pytest.raises(e.AuthException):
        auth.create_token(grant_type="bogus")


def test_create_token_refresh_flag_and_default_token():
    # An invalid `refresh` value falls back to 'yes', and omitting refresh_token
    # on a refresh_token grant falls back to the stored one -- both checked in
    # one real round trip to avoid hammering the live auth endpoint.
    # Success returns the raw OAuth2 token payload, not the usual status/response envelope.
    response = auth.create_token(grant_type="refresh_token", refresh="bogus")
    assert "access_token" in response
    assert "refresh_token" in response


class _Handler(http.server.BaseHTTPRequestHandler):
    status = 200
    body = b"{}"

    def do_POST(self):
        self.send_response(self.status)
        self.send_header("Content-Length", str(len(self.body)))
        self.end_headers()
        self.wfile.write(self.body)

    def log_message(self, *args):
        pass


def _run_server(status, body=b"{}"):
    _Handler.status = status
    _Handler.body = body
    server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_create_token_connection_error():
    with patch("sonetel._constants.API_URI_AUTH", "http://127.0.0.1:1"):
        response = auth.create_token(grant_type="password")
    assert response["status"] == "failed"
    assert response["error"] == "ConnectionError"


def test_create_token_http_error():
    server = _run_server(status=400, body=b'{"error": "bad request"}')
    try:
        with patch(
            "sonetel._constants.API_URI_AUTH", f"http://127.0.0.1:{server.server_port}/"
        ):
            response = auth.create_token(grant_type="password")
        assert response["status"] == "failed"
        assert (
            response["error"] == "Timeout"
        )  # mislabeled in auth.py's HTTPError branch
    finally:
        server.shutdown()
        server.server_close()


def test_create_token_unexpected_status():
    server = _run_server(status=201)
    try:
        with patch(
            "sonetel._constants.API_URI_AUTH", f"http://127.0.0.1:{server.server_port}/"
        ):
            response = auth.create_token(grant_type="password")
        assert response["status"] == "failed"
        assert response["error"] == "Unknown error"
    finally:
        server.shutdown()
        server.server_close()
