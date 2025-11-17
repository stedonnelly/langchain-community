import logging
from typing import Type

from langchain_community.tools.windy.base import WindyBaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, Field
from windy_api.models.point_request import Levels, ModelTypes, ValidParameters
from windy_api.schema.schema import WindyForecastResponse


class PointRequestSchema(BaseModel):
    """Input schema for point forecast request."""

    latitude: float = Field(ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(ge=-180, le=180, description="Longitude coordinate")
    model: ModelTypes = Field(
        default=ModelTypes.GFS, description="Forecast model to use"
    )
    parameters: list[ValidParameters] = Field(
        default=[ValidParameters.TEMP],
        description="Parameters to retrieve from the forecast",
    )
    levels: list[Levels] = Field(
        default=[Levels.SURFACE],
        description="Atmospheric levels (e.g., 'surface', '850h')",
    )


class WindyGetPointForecast(WindyBaseTool):
    """Tool that gets point forecast from Windy API."""

    name: str = "get_point_forecast"
    description: str = (
        "Use this tool to get a point weather forecast for a specific location."
    )
    args_schema: Type[PointRequestSchema] = PointRequestSchema

    def _run(
        self,
        latitude: float,
        longitude: float,
        model: ModelTypes = ModelTypes.GFS,
        parameters: list[ValidParameters] = [ValidParameters.TEMP],
        levels: list[Levels] = [Levels.SURFACE],
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> WindyForecastResponse | str:
        try:
            forecast = self.api.get_point_forecast(
                latitude=latitude,
                longitude=longitude,
                model=model,
                parameters=parameters,
                levels=levels,
            )
            return forecast
        except Exception as e:
            logging.getLogger(__name__)
            err_str = f"Error fetching point forecast: {e}"
            return err_str
