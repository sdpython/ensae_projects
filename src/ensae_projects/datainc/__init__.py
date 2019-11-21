"""
@file
@brief  Shortcuts to data
"""

from .data_exception import PasswordException
from .data_helper import (
    change_encoding,
    change_encoding_improve,
    clean_column_name_sql_dump,
    convert_dates,
    enumerate_text_lines,
)
from .datazips import besancon_df
from .data_medical import convert_dcm2png
