from unittest.mock import Mock, patch

import pytest

from py_tata.tasks import TaskResult
from py_tata.tasks.check_hostname.task import CheckHostnameTask


@pytest.mark.asyncio
class TestCheckHostnameTask:
    def setup_method(self):
        self.target_hostname = "test-target"
        self.sut = CheckHostnameTask(self.target_hostname)

    @patch("py_tata.tasks.check_hostname.task.platform.node")
    async def test_check_fail(self, platform_node_mock: Mock):
        current_hostname = f"not-{self.sut.target_hostname}"
        platform_node_mock.return_value = current_hostname

        result = await self.sut.check()

        assert result == TaskResult(
            description=f"Check hostname is {self.target_hostname}",
            errors=[
                f"Incorrect hostname: "
                f"Expected {self.sut.target_hostname} but hostname is {current_hostname} now",
            ],
        )

    @patch("py_tata.tasks.check_hostname.task.platform.node")
    async def test_check_success(self, platform_node_mock: Mock):
        current_hostname = self.sut.target_hostname
        platform_node_mock.return_value = current_hostname

        result = await self.sut.check()

        assert result == TaskResult(
            description=f"Check hostname is {self.sut.target_hostname}",
            errors=[],
        )
