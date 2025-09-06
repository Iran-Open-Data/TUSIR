# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=too-many-locals

from typing import Any, Iterable, Optional, Literal, overload
from pathlib import Path

import pandas as pd

from bssir.metadata_reader import config
from bssir.api import API


defaults, metadata = config.set_package_config(Path(__file__).parent)
api = API(defaults=defaults, metadata=metadata)

_Years = Optional[Literal[1387, 1393, 1398, "all", "last"]]


def __get_optional_params(local_variables: dict) -> dict:
    return {key: value for key, value in local_variables.items() if value is not None}


def setup_raw_data(
    years: _Years = "all",
    replace: Optional[bool] = None,
    download_source: Optional[Literal["original", "mirror"] | str] = None,
) -> None:
    parameters = __get_optional_params(locals())
    api.setup_raw_data(**parameters)
