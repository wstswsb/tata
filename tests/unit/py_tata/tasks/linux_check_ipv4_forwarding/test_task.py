from unittest.mock import AsyncMock, Mock, patch

import pytest

import py_tata.tasks.linux_check_ipv4_forwarding as linux_check_ipv4_forwarding
from py_tata.core.command_executor import AsyncioCommandExecutor
from py_tata.core.command_executor.asyncio_command_executor import CommandResult
from py_tata.tasks import TaskResult


@pytest.mark.asyncio
class TestLinuxCheckIPForwarding:
    def setup_method(self):
        self.command_executor_mock = Mock(spec=AsyncioCommandExecutor)
        self.sut = linux_check_ipv4_forwarding.LinuxCheckIPv4ForwardingTask(
            asyncio_command_executor=self.command_executor_mock,
            enabled=True,
        )

    @patch("py_tata.tasks.linux_check_ipv4_forwarding.task.platform.system")
    async def test_check_on_windows_with_error(self, system_mock: Mock):
        system_mock.return_value = "Windows"

        result = await self.sut.check()

        assert result == TaskResult(
            description="Check ip forwarding is enabled",
            errors=["Not supported system. Only Linux support"],
        )

        system_mock.assert_called_once()

    @patch("py_tata.tasks.linux_check_ipv4_forwarding.task.platform.system")
    async def test_check_ipv4_forwarding_enabled(self, system_mock: Mock):
        system_mock.return_value = "Linux"
        self.command_executor_mock.execute = AsyncMock(
            return_value=CommandResult(
                return_code=0,
                stdout="1",
                stderr="",
            )
        )
        result = await self.sut.check()

        assert result == TaskResult(
            description="Check ip forwarding is enabled",
            errors=[],
        )

    @patch("py_tata.tasks.linux_check_ipv4_forwarding.task.platform.system")
    async def test_check_ipv4_forwarding_disabled(self, system_mock: Mock):
        system_mock.return_value = "Linux"
        self.command_executor_mock.execute = AsyncMock(
            return_value=CommandResult(
                return_code=0,
                stdout="0",
                stderr="",
            )
        )
        result = await self.sut.check()

        assert result == TaskResult(
            description="Check ip forwarding is enabled",
            errors=["IPv4 forwarding disabled"],
        )
