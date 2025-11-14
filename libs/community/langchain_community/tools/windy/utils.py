"""Utility functions for the Windy toolkit."""

import os
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from windy_api import WindyAPI


def get_api_key() -> "WindyAPI":
    """Retrieve the Windy API key from environment variables."""
    try:
        from windy_api import WindyAPI
    except ImportError as e:
        raise ImportError(
            "windy_api package is not installed. Please install the windy package with `pip install windy_api`."
        ) from e
    if "WINDY_API_KEY" not in os.environ:
        raise ValueError(
            "Please set the WINDY_API_KEY environment variable with your Windy API key."
        )
    api_key = os.environ["WINDY_API_KEY"]
    client = WindyAPI(api_key=api_key)
    logging.info("WindyAPI client created successfully.")
    return client
