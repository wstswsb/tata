from typing import get_args

from .builder import check_hostname_task_builder
from .validation_model import CheckHostnameIn

TASK_NAME = get_args(CheckHostnameIn.__annotations__["task"])[0]
builder = check_hostname_task_builder
TASK_NAME_TO_BUILDER = {TASK_NAME: builder}
