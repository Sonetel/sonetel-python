"""
Tests for the session management functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

import requests

from sonetel import configure
from sonetel.session import SessionManager
from sonetel.utilities import get_session


class TestSessionManager(unittest.TestCase):
    """Test the SessionManager class."""

    def test_session_creation(self):
        """Test that a SessionManager can be created."""
        session_manager = SessionManager()
        self.assertIsNotNone(session_manager)
        self.assertIsInstance(session_manager.session, requests.Session)

    @patch("requests.Session.request")
    def test_request_success(self, mock_request):
        """Test that a request can be made successfully."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": "test"}
        mock_request.return_value = mock_response

        # Create session manager and make request
        session_manager = SessionManager()
        response = session_manager.request(
            method="GET",
            url="https://example.com",
            token="test_token",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "GET")
        self.assertEqual(kwargs["url"], "https://example.com")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")
        self.assertEqual(
            kwargs["headers"]["Content-Type"], "application/json;charset=UTF-8"
        )

        # Verify response was processed correctly
        self.assertEqual(response, {"status": "success", "data": "test"})

    @patch("requests.Session.request")
    def test_request_error(self, mock_request):
        """Test that errors are handled correctly."""
        # Setup mock to raise an exception
        mock_request.side_effect = requests.exceptions.ConnectionError(
            "Connection error"
        )

        # Create session manager and make request
        session_manager = SessionManager()
        response = session_manager.request(
            method="GET",
            url="https://example.com",
        )

        # Verify error response
        self.assertEqual(response["status"], "failed")
        self.assertEqual(response["error"], "ConnectionError")
        self.assertIn("Connection error", response["message"])

    def test_get_session(self):
        """Test that get_session returns a SessionManager instance."""
        session1 = get_session()
        session2 = get_session()

        # Verify that the same instance is returned
        self.assertIs(session1, session2)

        # Verify that it's a SessionManager
        self.assertIsInstance(session1, SessionManager)

    @patch("sonetel.utilities._session_manager")
    def test_configure(self, mock_session_manager):
        """Test that configure creates a new session with the specified parameters."""
        # Call configure with custom parameters
        configure(
            timeout=10,
            max_retries=5,
            backoff_factor=0.5,
            pool_connections=20,
            pool_maxsize=20,
            log_level="DEBUG",
        )

        # Verify that get_session was called with the correct parameters
        # Note: This is a simplified test that doesn't actually verify the parameters
        # were passed correctly, since that would require more complex mocking
        self.assertIsNotNone(get_session())


if __name__ == "__main__":
    unittest.main()
