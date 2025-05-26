"""
Session management for Sonetel API requests.
"""

import logging
import time
from typing import Any, Dict, Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import _constants as const
from . import exceptions as e


class SessionManager:
    """
    Manages HTTP sessions and requests for the Sonetel API.
    Provides connection pooling, retry logic, and consistent error handling.
    """

    def __init__(
        self,
        timeout: Union[float, Tuple[float, float]] = (3.05, 60),
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Tuple = (500, 502, 503, 504),
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ):
        """
        Initialize the session manager with configurable parameters.

        Args:
            timeout: Request timeout (connect_timeout, read_timeout) in seconds
            max_retries: Maximum number of retries for failed requests
            backoff_factor: Backoff factor for retries (exponential backoff)
            status_forcelist: HTTP status codes that should trigger a retry
            pool_connections: Number of connection pools to cache
            pool_maxsize: Maximum number of connections to save in the pool
        """
        self.session = requests.Session()
        self.timeout = timeout

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["GET", "PUT", "DELETE", "POST", "PATCH"],
        )

        # Mount the retry adapter to the session
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Add default headers
        self.session.headers.update(
            {"User-Agent": f"Sonetel Python Package - v{const.PKG_VERSION}"}
        )

        self.logger = logging.getLogger(__name__)

    def request(
        self,
        method: str,
        url: str,
        token: Optional[str] = None,
        body: Optional[str] = None,
        content_type: str = const.CONTENT_TYPE_GENERAL,
        auth: Optional[Tuple[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Send an HTTP request to the Sonetel API with proper error handling and logging.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: API endpoint URL
            token: OAuth access token (for authenticated requests)
            body: Request body (JSON string)
            content_type: Content type header
            auth: Basic auth tuple (username, password)

        Returns:
            API response as a dict

        Raises:
            SonetelException: For API errors and connection issues
        """
        headers = {"Content-Type": content_type}

        # Add authorization if token is provided
        if token:
            headers["Authorization"] = f"Bearer {token}"

        start_time = time.time()

        try:
            self.logger.debug("Sending %s request to %s", method, url)

            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=body,
                auth=auth,
                timeout=self.timeout,
            )

            # Raise HTTPError for bad response codes
            response.raise_for_status()

            # Log request duration
            duration = time.time() - start_time
            self.logger.debug("Request completed in %ss", format(duration, ".2f"))

            # Return JSON response if available
            if response.status_code == requests.codes.ok:
                return response.json()

            # Should not get here due to raise_for_status
            return {"status": "unknown", "response": response.text}

        except requests.exceptions.HTTPError as err:
            self.logger.error("HTTP Error: %s", err)
            return {
                "status": "failed",
                "error": "HTTPError",
                "message": err.response.text,
            }

        except requests.exceptions.ConnectionError as err:
            self.logger.error("Connection Error: %s", err)
            return {"status": "failed", "error": "ConnectionError", "message": str(err)}

        except requests.exceptions.Timeout as err:
            self.logger.error("Timeout Error: %s", err)
            return {
                "status": "failed",
                "error": "Timeout",
                "message": "Request timed out",
            }

        except requests.exceptions.RequestException as err:
            self.logger.error("Request Exception: %s", err)
            return {
                "status": "failed",
                "error": "RequestException",
                "message": str(err),
            }

    def close(self):
        """Close the session and release resources."""
        self.session.close()
