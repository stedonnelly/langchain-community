"""Base class for Windy toolkits and tools."""

from typing import TYPE_CHECKING
from langchain_core.tools import BaseTool
from pydantic import ConfigDict, Field

from langchain_community.tools.windy.utils import get_api_key

if TYPE_CHECKING:
    # This is for linting and type hints
    from windy_api import WindyAPI
else:
    try:
        from windy_api import WindyAPI
    except ImportError:
        pass


class WindyBaseTool(BaseTool):
    """Base class for Windy tools."""

    api: WindyAPI = Field(
        default_factory=get_api_key, description="An instance of the WindyAPI client."
    )
