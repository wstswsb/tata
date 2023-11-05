import asyncio
from typing import Protocol

from src.tasks import TaskResult


class TaskProtocol(Protocol):
    async def check(self) -> TaskResult:
        ...


class Runner:
    def __init__(self, tasks: list[TaskProtocol]):
        self.tasks = tasks

    async def run(self) -> list[TaskResult]:
        asyncio_tasks = []
        for task in self.tasks:
            asyncio_tasks.append(asyncio.create_task(task.check()))

        return await asyncio.gather(*asyncio_tasks)
