import asyncio
from collections.abc import Coroutine, Iterable
from typing import Protocol

from src.tasks import TaskResult


class TaskProtocol(Protocol):
    async def check(self) -> TaskResult:
        ...


class Runner:
    def __init__(self, tasks: list[TaskProtocol]):
        self.tasks = tasks

    def run(self) -> Iterable[Coroutine[None, None, TaskResult]]:
        asyncio_tasks = []
        for task in self.tasks:
            asyncio_tasks.append(asyncio.create_task(task.check()))

        for coro in asyncio.as_completed(asyncio_tasks):
            yield coro
