from typing import TypeVar

import pydantic

from py_tata.core.builder.task_builder import TaskBuilder
from py_tata.core.command_executor import AsyncioCommandExecutor

T = TypeVar("T")


class LinuxCheckForwardingTaskBuilder(TaskBuilder):
    def __init__(self, command_executor: AsyncioCommandExecutor, task_class: T):
        super().__init__(task_class)
        self.command_executor = command_executor

    def build(
        self,
        model_in: pydantic.BaseModel,
    ) -> T:
        return self.task_class(
            **model_in.model_dump(),
            asyncio_command_executor=self.command_executor,
        )
