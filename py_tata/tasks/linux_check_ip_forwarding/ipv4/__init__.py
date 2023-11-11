from typing import get_args

from .builder import task_builder
from .task import LinuxCheckIPv4ForwardingTask
from .validation_model import LinuxCheckIPv4ForwardingIn

TASK_NAME = get_args(LinuxCheckIPv4ForwardingIn.__annotations__["task"])[0]
builder = task_builder
TASK_NAME_TO_BUILDER = {TASK_NAME: builder}
