from unittest.mock import AsyncMock, Mock

import pytest

from src.tasks import TaskResult
from src.tasks.runner import Runner


@pytest.mark.asyncio
class TestRunner:
    def __build_task_mock(self, description: str, errors: list[str]):
        return Mock(
            check=AsyncMock(
                return_value=TaskResult(description=description, errors=errors)
            )
        )

    async def test_run(self):
        task_mocks = [
            self.__build_task_mock(description="Task-1", errors=[]),
            self.__build_task_mock(description="Task-2", errors=["1"]),
        ]

        sut = Runner(task_mocks)

        results = [await coro for coro in sut.run()]

        assert results == [TaskResult("Task-1", []), TaskResult("Task-2", ["1"])]
