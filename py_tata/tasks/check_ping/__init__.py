from typing import get_args

from .builder import check_ping_task_builder
from .task import CheckPingTask
from .validation_model import CheckPingIn

TASK_NAME = get_args(CheckPingIn.__annotations__["task"])[0]
builder = check_ping_task_builder
TASK_NAME_TO_BUILDER = {TASK_NAME: builder}
