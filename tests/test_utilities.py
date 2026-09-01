"""
Tests for sonetel.utilities: pure functions, local validation branches,
and network-error branches of send_api_request() against a real local
HTTP server (no live Sonetel API calls needed for any of these).
"""

import http.server
import threading

import jwt
import pytest

from sonetel import exceptions as e
from sonetel.utilities import (
    Resource,
    date_diff,
    is_valid_date,
    prepare_error,
    send_api_request,
)


def _expired_token():
    return jwt.encode(
        {"acc_id": "1234", "user_id": "5678", "exp": 1, "aud": "api.sonetel.com"},
        key="test-secret-key-at-least-32-bytes-long",
        algorithm="HS256",
    )


def test_resource_requires_access_token():
    with pytest.raises(e.AuthException):
        Resource(access_token="")


def test_resource_rejects_expired_token():
    with pytest.raises(e.AuthException):
        Resource(access_token=_expired_token())


def test_is_valid_date_rejects_bad_format():
    assert is_valid_date("not-a-date") is False


def test_is_valid_date_accepts_correct_format():
    assert is_valid_date("20230101T00:00:00Z") is True


def test_date_diff():
    assert date_diff("20230101T00:00:00Z", "20230102T00:00:00Z") is True
    assert date_diff("20230102T00:00:00Z", "20230101T00:00:00Z") is False


def test_prepare_error():
    assert prepare_error(code=1000, message="boom") == {
        "status": "failed",
        "code": 1000,
        "message": "boom",
    }


def test_send_api_request_requires_token():
    with pytest.raises(e.SonetelException):
        send_api_request(token="", uri="http://example.com")


def test_send_api_request_requires_uri():
    with pytest.raises(e.SonetelException):
        send_api_request(token="x", uri="")


def test_send_api_request_generic_exception_on_malformed_url():
    response = send_api_request(token="x", uri="not-a-url")
    assert response["status"] == "failed"
    assert response["error"] == "RequestException"


def test_send_api_request_connection_error():
    response = send_api_request(token="x", uri="http://127.0.0.1:1")
    assert response["status"] == "failed"
    assert response["error"] == "ConnectionError"


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(201)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *args):
        pass


def test_send_api_request_non_200_status_returns_none():
    server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        response = send_api_request(
            token="x", uri=f"http://127.0.0.1:{server.server_port}/"
        )
        assert response is None
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    pytest.main()
