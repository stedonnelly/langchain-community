"""Unit tests for WindyToolkit."""

from unittest.mock import Mock, patch
import pytest
from langchain_community.agent_toolkits.windy.toolkit import WindyToolkit
from langchain_community.tools.windy.get_point_forecast import WindyGetPointForecast


@pytest.fixture
def mock_windy_api():
    """Create a mock WindyAPI instance."""
    mock_api = Mock()
    return mock_api


def test_windy_toolkit_instantiation(mock_windy_api):
    """Test WindyToolkit can be instantiated."""
    toolkit = WindyToolkit(api=mock_windy_api)
    assert toolkit is not None
    assert toolkit.api == mock_windy_api


def test_windy_toolkit_get_tools(mock_windy_api):
    """Test WindyToolkit returns the correct tools."""
    toolkit = WindyToolkit(api=mock_windy_api)
    tools = toolkit.get_tools()

    assert isinstance(tools, list)
    assert len(tools) == 1
    assert isinstance(tools[0], WindyGetPointForecast)


def test_windy_toolkit_tool_names(mock_windy_api):
    """Test WindyToolkit tools have expected names."""
    toolkit = WindyToolkit(api=mock_windy_api)
    tools = toolkit.get_tools()

    tool_names = [tool.name for tool in tools]
    assert "get_point_forecast" in tool_names


@patch("langchain_community.agent_toolkits.windy.toolkit.get_api_key")
def test_windy_toolkit_default_api_creation(mock_get_api_key):
    """Test WindyToolkit creates API client by default."""
    mock_api = Mock()
    mock_get_api_key.return_value = mock_api

    toolkit = WindyToolkit()

    assert toolkit.api == mock_api
    mock_get_api_key.assert_called_once()
