import pytest

from src.tasks import TaskResult
from src.tasks.check_ping import CheckPingTask


@pytest.mark.asyncio
class TestCheckPingTask:
    async def test_ping_accessible(self):
        sut = CheckPingTask(target_ip="127.0.0.1")

        result = await sut.check()

        assert result == TaskResult(
            description=f"Check ping for ip={sut.target_ip}",
            errors=[],
        )

    async def test_ping_not_accessible(self):
        sut = CheckPingTask(target_ip="192.168.40.40")

        result = await sut.check()

        assert result == TaskResult(
            description=f"Check ping for ip={sut.target_ip}",
            errors=[f"Cannot ping host with ip={sut.target_ip}"],
        )
