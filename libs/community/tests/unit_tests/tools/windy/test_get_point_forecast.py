"""Unit tests for WindyGetPointForecast tool."""

from unittest.mock import Mock, patch
import pytest
from langchain_community.tools.windy.get_point_forecast import (
    WindyGetPointForecast,
    PointRequestSchema,
)
from windy_api.models.point_request import (
    Levels,
    ModelTypes,
    ValidParameters,
)


@pytest.fixture
def mock_windy_api():
    """Create a mock WindyAPI instance."""
    mock_api = Mock()
    return mock_api


@pytest.fixture
def mock_forecast_response():
    """Create a mock forecast response with dummy data."""
    mock_response = Mock()
    mock_response.ts = [1699000000, 1699003600, 1699007200]  # Dummy timestamps
    mock_response.data = {
        "temp-surface": [15.5, 16.2, 17.1]  # Dummy temperature data
    }
    return mock_response


def test_point_request_schema_defaults():
    """Test PointRequestSchema has correct default values."""
    schema = PointRequestSchema(latitude=51.5, longitude=-0.1)

    assert schema.latitude == 51.5
    assert schema.longitude == -0.1
    assert schema.model == ModelTypes.GFS
    assert schema.parameters == [ValidParameters.TEMP]
    assert schema.levels == [Levels.SURFACE]


def test_point_request_schema_validation():
    """Test PointRequestSchema validates latitude and longitude bounds."""
    # Valid coordinates
    schema = PointRequestSchema(latitude=51.5, longitude=-0.1)
    assert schema.latitude == 51.5
    assert schema.longitude == -0.1

    # Test latitude bounds
    with pytest.raises(ValueError):
        PointRequestSchema(latitude=91, longitude=0)

    with pytest.raises(ValueError):
        PointRequestSchema(latitude=-91, longitude=0)

    # Test longitude bounds
    with pytest.raises(ValueError):
        PointRequestSchema(latitude=0, longitude=181)

    with pytest.raises(ValueError):
        PointRequestSchema(latitude=0, longitude=-181)


def test_windy_get_point_forecast_tool_name(mock_windy_api):
    """Test WindyGetPointForecast has correct name."""
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)
    assert tool.name == "get_point_forecast"


def test_windy_get_point_forecast_tool_description(mock_windy_api):
    """Test WindyGetPointForecast has a description."""
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)
    assert "point weather forecast" in tool.description.lower()


def test_windy_get_point_forecast_success(mock_windy_api, mock_forecast_response):
    """Test WindyGetPointForecast returns forecast data successfully."""
    # Setup mock
    mock_windy_api.get_point_forecast.return_value = mock_forecast_response

    # Create tool and run
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)
    result = tool._run(
        latitude=51.5,
        longitude=-0.1,
        model=ModelTypes.GFS,
        parameters=[ValidParameters.TEMP],
        levels=[Levels.SURFACE],
    )

    # Verify API was called correctly
    mock_windy_api.get_point_forecast.assert_called_once_with(
        latitude=51.5,
        longitude=-0.1,
        model=ModelTypes.GFS,
        parameters=[ValidParameters.TEMP],
        levels=[Levels.SURFACE],
    )

    # Verify result
    assert result == mock_forecast_response
    assert hasattr(result, "ts")
    assert hasattr(result, "data")


def test_windy_get_point_forecast_with_multiple_parameters(
    mock_windy_api, mock_forecast_response
):
    """Test WindyGetPointForecast with multiple weather parameters."""
    # Setup mock
    mock_windy_api.get_point_forecast.return_value = mock_forecast_response

    # Create tool and run with multiple parameters
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)
    result = tool._run(
        latitude=40.7,
        longitude=-74.0,
        model=ModelTypes.GFS,
        parameters=[ValidParameters.TEMP, ValidParameters.WIND, ValidParameters.RH],
        levels=[Levels.SURFACE],
    )

    # Verify API was called with multiple parameters
    mock_windy_api.get_point_forecast.assert_called_once()
    call_kwargs = mock_windy_api.get_point_forecast.call_args[1]
    assert ValidParameters.TEMP in call_kwargs["parameters"]
    assert ValidParameters.WIND in call_kwargs["parameters"]
    assert ValidParameters.RH in call_kwargs["parameters"]


def test_windy_get_point_forecast_error_handling(mock_windy_api):
    """Test WindyGetPointForecast handles API errors gracefully."""
    # Setup mock to raise an exception
    mock_windy_api.get_point_forecast.side_effect = Exception("API Error")

    # Create tool and run
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)
    result = tool._run(
        latitude=51.5,
        longitude=-0.1,
        model=ModelTypes.GFS,
        parameters=[ValidParameters.TEMP],
        levels=[Levels.SURFACE],
    )

    # Verify error message is returned
    assert isinstance(result, str)
    assert "Error fetching point forecast" in result
    assert "API Error" in result


def test_windy_get_point_forecast_different_locations(
    mock_windy_api, mock_forecast_response
):
    """Test WindyGetPointForecast works with different geographic locations."""
    mock_windy_api.get_point_forecast.return_value = mock_forecast_response
    tool = WindyGetPointForecast.model_construct(api=mock_windy_api)

    # Test different locations
    locations = [
        (51.5074, -0.1278),  # London
        (40.7128, -74.0060),  # New York
        (35.6762, 139.6503),  # Tokyo
        (-33.8688, 151.2093),  # Sydney
    ]

    for lat, lon in locations:
        result = tool._run(
            latitude=lat,
            longitude=lon,
            model=ModelTypes.GFS,
            parameters=[ValidParameters.TEMP],
            levels=[Levels.SURFACE],
        )
        assert result == mock_forecast_response
