import platform

from py_tata.core.command_executor import AsyncioCommandExecutor
from py_tata.tasks.task_result import TaskResult


class LinuxCheckIPv4ForwardingTask:
    def __init__(
        self,
        asyncio_command_executor: AsyncioCommandExecutor,
        enabled: bool,
        **kwargs,
    ):
        self.asyncio_command_executor = asyncio_command_executor
        self.enabled = enabled

    @property
    def task_description(self):
        return f"Check ip forwarding is {'enabled' if self.enabled else 'disabled'}"

    async def check(self):
        if platform.system() != "Linux":
            return TaskResult(
                description=self.task_description,
                errors=["Not supported system. Only Linux support"],
            )

        errors = []
        try:
            command = ("sysctl", "-n", "net.ipv4.ip_forward")
            command_result = await self.asyncio_command_executor.execute(*command)
            if command_result.return_code != 0:
                errors.append("Failed to check configuration with sysctl")
            if self.enabled and int(command_result.stdout) != 1:
                errors.append("IPv4 forwarding disabled")
            if not self.enabled and int(command_result.stdout) != 0:
                errors.append("IPv4 forwarding enabled")

        except Exception as e:
            errors.append(str(e))

        return TaskResult(description=self.task_description, errors=errors)
