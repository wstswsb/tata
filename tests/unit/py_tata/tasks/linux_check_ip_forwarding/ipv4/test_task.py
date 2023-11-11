from unittest.mock import Mock

from py_tata.core.command_executor import AsyncioCommandExecutor
from py_tata.tasks.linux_check_ip_forwarding.ipv4 import LinuxCheckIPv4ForwardingTask


class TestLinuxCheckIPv4ForwardingTask:
    def setup_method(self):
        self.command_executor_mock = Mock(spec=AsyncioCommandExecutor)
        self.sut = LinuxCheckIPv4ForwardingTask(
            asyncio_command_executor=self.command_executor_mock,
            enabled=True,
        )

    def test_status_check_command(self):
        assert self.sut.status_check_command == ("sysctl", "-n", "net.ipv4.ip_forward")

    def test_ip_version(self):
        assert self.sut.ip_version == "IPv4"
