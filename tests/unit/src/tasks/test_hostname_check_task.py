from unittest.mock import Mock, patch

from src.tasks import HostnameCheckTask, TaskResult


class TestHostnameCheckTask:
    def setup(self):
        self.sut = HostnameCheckTask()

    @patch("src.tasks.hostname_check_task.platform.node")
    def test_check_fail(self, platform_node_mock: Mock):
        target_hostname = "test-target"
        current_hostname = f"not-{target_hostname}"
        platform_node_mock.return_value = current_hostname

        result = self.sut.check(target_hostname)

        assert result == TaskResult(
            description=f"Check hostname is {target_hostname}",
            errors=[
                f"Incorrect hostname: "
                f"Expected {target_hostname} but hostname is {current_hostname} now",
            ],
        )

    @patch("src.tasks.hostname_check_task.platform.node")
    def test_check_success(self, platform_node_mock: Mock):
        target_hostname = "test-target"
        current_hostname = target_hostname
        platform_node_mock.return_value = current_hostname

        result = self.sut.check(target_hostname)

        assert result == TaskResult(
            description=f"Check hostname is {target_hostname}",
            errors=[],
        )
