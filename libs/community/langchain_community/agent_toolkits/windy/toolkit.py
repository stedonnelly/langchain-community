from typing import TYPE_CHECKING, List

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit
from pydantic import ConfigDict, Field
from langchain_community.tools.windy import get_api_key
from langchain_community.tools.windy import WindyGetPointForecast

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from windy_api import WindyAPI
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from windy_api import WindyAPI
    except ImportError:
        pass


class WindyToolkit(BaseToolkit):
    """Toolkit for interacting with the Windy API.

    Parameters:
        api_key: The Windy API key.

    Setup:
        Install the Windy API client and set the environment variable ``WINDY_API_KEY`` with your Windy API key.
        .. code-block:: bash

            pip install -U windy_api
            export WINDY_API_KEY="your-windy-api-key"

    Key init args:
        api: windy_api.WindyAPI
            An instance of the WindyAPI client.

    Instantiate:
        .. code-block:: python

            from langchain_community.agent_toolkits import WindyToolkit

            toolkit = WindyToolkit()

    Available Tools:
        Currently the toolkit provides the following tools:
        - WindyGetPointForecast: Get weather forecast for a specific point.

        .. code-block:: python
            tools = toolkit.get_tools()
            tools

        .. code-block:: none
            [WindyGetPointForecast(api=<windy_api.api.api.WindyAPI object at 0x10dbaccd0>)]

    Using this Toolkit with an Agent:
        .. code-block:: python
            from langchain.agents import create_agent
            from langchain_community.agent_toolkits import WindyToolkit

            toolkit = WindyToolkit()
            tools = toolkit.get_tools()
            agent = create_agent(
                model="gpt-5-nano",
                tools=tools,
            )

            response = agent.invoke({"messages": [{"role": "user", "content": "What's the temperature going to be like in Bristol, UK over the next 3 days?"}]})
            print(response)
    """

    api: WindyAPI = Field(
        default_factory=get_api_key,
        description="An instance of the WindyAPI client.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools for the toolkit."""
        return [WindyGetPointForecast()]
