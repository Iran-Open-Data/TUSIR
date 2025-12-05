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
_Table = Literal[
    "form_1_master",
    "form_1_detail",
    "form_2_master",
    "form_2_detail",
]


def __get_optional_params(local_variables: dict) -> dict:
    return {key: value for key, value in local_variables.items() if value is not None}


def setup_raw_data(
    years: _Years = "all",
    replace: Optional[bool] = None,
    download_source: Optional[Literal["original", "mirror"] | str] = None,
) -> None:
    """Download and extract raw survey data for the requested years.

    High-level convenience method for obtaining the original (unprocessed)
    survey tables. Downloads the necessary archive files for the given year
    or years, unpacks them, and extracts each data table as CSV files into
    the package's configured data directories.

    Parameters
    ----------
    years : _Years, optional
        Year (e.g. 1387), an iterable of years, or a supported keyword:
        - "all": download and extract all available years
        - "last": download and extract the most recent available year
        Defaults to "all".
    replace : bool, optional
        If True, overwrite any existing extracted files. If False, existing
        files are preserved. If None, the package default behavior is used.
    download_source : {"original", "mirror"} or str, optional
        Select the download source. Common values are "original" or "mirror".
        A named source supported by the underlying API may be provided.

    Returns
    -------
    None
        Files are written to the package's configured data directories.

    Raises
    ------
    ValueError
        If the provided `years` value is invalid.
    OSError, IOError
        On network, filesystem, or extraction errors raised by the underlying
        API. Exceptions from api.setup_raw_data are propagated to the caller.

    Examples
    --------
    ```python
        # download and extract all years (default)
        setup_raw_data()
    ```

    ```python
        # download only year 1398 and overwrite existing files
        setup_raw_data(years=1398, replace=True)
    ```

    ```python
        # use the mirror download source for the last available year
        setup_raw_data(years="last", download_source="mirror")
    ```
    """
    parameters = __get_optional_params(locals())
    api.setup_raw_data(**parameters)


def load_table(
    table_name: _Table,
    years: _Years = None,
    form: Literal["normalized", "cleaned", "raw"] | None = None,
    *,
    on_missing: Literal["error", "download", "create"] | None = None,
    redownload: bool | None = None,
    save_downloaded: bool | None = None,
    recreate: bool | None = None,
    save_created: bool | None = None,
) -> pd.DataFrame:
    api.metadata.reload()
    parameters = __get_optional_params(locals())
    return api.load_table(**parameters)
