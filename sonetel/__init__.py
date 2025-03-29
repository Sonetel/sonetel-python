"""
Sonetel Python SDK

A Python package for using Sonetel's REST API endpoints.
"""

import atexit
import logging
from typing import Optional, Tuple, Union

from .account import Account
from .auth import Auth
from .calls import Call
from .phonenumber import PhoneNumber
from .recording import Recording
from .users import User
from .utilities import get_session
from .voiceapps import VoiceApp

# Configure package-level logger
logger = logging.getLogger(__name__)

__version__ = "0.3.0"


def configure(
    timeout: Union[float, Tuple[float, float]] = (3.05, 60),
    max_retries: int = 3,
    backoff_factor: float = 0.3,
    pool_connections: int = 10,
    pool_maxsize: int = 10,
    log_level: Optional[str] = None,
):
    """
    Configure the Sonetel SDK with custom parameters.

    Args:
        timeout: Request timeout in seconds. Can be a single float or a tuple of (connect_timeout, read_timeout)
        max_retries: Maximum number of retries for failed requests
        backoff_factor: Backoff factor for retries (exponential backoff)
        pool_connections: Number of connection pools to cache
        pool_maxsize: Maximum number of connections to save in the pool
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Configure logging
    if log_level:
        logging.basicConfig(level=getattr(logging, log_level))
        logger.setLevel(getattr(logging, log_level))

    # Get session with custom parameters
    get_session(
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
        pool_connections=pool_connections,
        pool_maxsize=pool_maxsize,
    )


# Register cleanup function for program exit
def _cleanup():
    """Close the session and release resources on program exit."""
    try:
        session = get_session()
        session.close()
        logger.debug("Sonetel SDK session closed")
    except Exception as e:
        logger.debug(f"Error during cleanup: {e}")


atexit.register(_cleanup)
