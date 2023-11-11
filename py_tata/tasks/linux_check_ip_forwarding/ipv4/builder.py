from py_tata.core.command_executor import asyncio_command_executor

from ..builder import LinuxCheckForwardingTaskBuilder
from .task import LinuxCheckIPv4ForwardingTask

task_builder = LinuxCheckForwardingTaskBuilder(
    command_executor=asyncio_command_executor,
    task_class=LinuxCheckIPv4ForwardingTask,
)
