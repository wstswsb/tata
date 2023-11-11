from unittest.mock import AsyncMock, Mock, patch

import pytest
from icmplib import Host, async_ping

import py_tata.tasks.check_ping as check_ping
from py_tata.tasks import TaskResult


@pytest.mark.asyncio
class TestCheckPingTask:
    @patch("py_tata.tasks.check_ping.task.async_ping", spec=async_ping)
    async def test_ping_accessible(self, async_ping_mock: AsyncMock):
        host_mock = Mock(spec=Host)
        host_mock.is_alive = True
        async_ping_mock.return_value = host_mock

        sut = check_ping.CheckPingTask(target_ip="127.0.0.1")

        result = await sut.check()

        assert result == TaskResult(
            description=f"Check ping for ip={sut.target_ip}",
            errors=[],
        )

        async_ping_mock.assert_awaited_once_with(
            sut.target_ip,
            count=3,
            privileged=False,
        )

    @patch("py_tata.tasks.check_ping.task.async_ping", spec=async_ping)
    async def test_ping_not_accessible(self, async_ping_mock: AsyncMock):
        host_mock = Mock(spec=Host)
        host_mock.is_alive = False
        async_ping_mock.return_value = host_mock

        sut = check_ping.CheckPingTask(target_ip="192.168.40.40")

        result = await sut.check()

        assert result == TaskResult(
            description=f"Check ping for ip={sut.target_ip}",
            errors=[f"Cannot ping host with ip={sut.target_ip}"],
        )
        async_ping_mock.assert_awaited_once_with(
            sut.target_ip,
            count=3,
            privileged=False,
        )
