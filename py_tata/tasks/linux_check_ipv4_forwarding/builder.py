import pydantic

from py_tata.core.builder.task_builder import TaskBuilder
from py_tata.core.command_executor import (
    AsyncioCommandExecutor,
    asyncio_command_executor,
)

from .task import LinuxCheckIPv4ForwardingTask
from .validation_model import LinuxCheckIPv4ForwardingIn


class LinuxCheckIPv4ForwardingTaskBuilder:
    def __init__(self, command_executor: AsyncioCommandExecutor):
        self.command_executor = command_executor

    def build(
        self,
        model_in: LinuxCheckIPv4ForwardingIn,
    ) -> LinuxCheckIPv4ForwardingTask:
        return LinuxCheckIPv4ForwardingTask(
            asyncio_command_executor=self.command_executor,
            enabled=model_in.enabled,
        )


task_builder = LinuxCheckIPv4ForwardingTaskBuilder(asyncio_command_executor)
