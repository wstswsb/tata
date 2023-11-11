from unittest.mock import Mock

from py_tata.core.command_executor import AsyncioCommandExecutor
from py_tata.tasks.linux_check_ip_forwarding.ipv6 import LinuxCheckIPv6ForwardingTask


class TestLinuxCheckIPv4ForwardingTask:
    def setup_method(self):
        self.command_executor_mock = Mock(spec=AsyncioCommandExecutor)
        self.sut = LinuxCheckIPv6ForwardingTask(
            asyncio_command_executor=self.command_executor_mock,
            enabled=True,
        )

    def test_status_check_command(self):
        assert self.sut.status_check_command == (
            "sysctl",
            "-n",
            "net.ipv6.conf.all" ".forwarding",
        )

    def test_ip_version(self):
        assert self.sut.ip_version == "IPv6"
