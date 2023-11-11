from typing import get_args

from .builder import task_builder
from .task import LinuxCheckIPv6ForwardingTask
from .validation_model import LinuxCheckIPv6ForwardingIn

TASK_NAME = get_args(LinuxCheckIPv6ForwardingIn.__annotations__["task"])[0]
builder = task_builder
TASK_NAME_TO_BUILDER = {TASK_NAME: builder}
