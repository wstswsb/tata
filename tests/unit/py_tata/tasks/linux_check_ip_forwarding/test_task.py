from unittest.mock import AsyncMock, Mock, patch

import pytest

from py_tata.core.command_executor import AsyncioCommandExecutor
from py_tata.core.command_executor.asyncio_command_executor import CommandResult
from py_tata.tasks import TaskResult
from py_tata.tasks.linux_check_ip_forwarding.task_abc import LinuxCheckIpForwardingTask


class LinuxCheckIpForwardingTaskImpl(LinuxCheckIpForwardingTask):
    @property
    def ip_version(self) -> str:
        return "IPv4"

    @property
    def status_check_command(self) -> tuple[str, ...]:
        return "test", "command"


@pytest.mark.asyncio
class TestLinuxCheckIPForwarding:
    def setup_method(self):
        self.command_executor_mock = Mock(spec=AsyncioCommandExecutor)
        self.sut = LinuxCheckIpForwardingTaskImpl(
            asyncio_command_executor=self.command_executor_mock,
            enabled=True,
        )

    @patch("py_tata.tasks.linux_check_ip_forwarding.task_abc.platform.system")
    async def test_check_on_windows_with_error(self, system_mock: Mock):
        system_mock.return_value = "Windows"

        result = await self.sut.check()

        assert result == TaskResult(
            description="Check IPv4 forwarding is enabled",
            errors=["Not supported system. Only Linux support"],
        )

        system_mock.assert_called_once()

    @patch("py_tata.tasks.linux_check_ip_forwarding.task_abc.platform.system")
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
            description="Check IPv4 forwarding is enabled",
            errors=[],
        )

    @patch("py_tata.tasks.linux_check_ip_forwarding.task_abc.platform.system")
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
            description="Check IPv4 forwarding is enabled",
            errors=["IPv4 forwarding disabled"],
        )
