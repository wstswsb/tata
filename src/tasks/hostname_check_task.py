import platform

from .task_result import TaskResult


class HostnameCheckTask:
    async def check(self, target: str) -> TaskResult:
        errors = []
        hostname = platform.node()
        if hostname != target:
            error = (
                f"Incorrect hostname: "
                f"Expected {target} but hostname is {hostname} now"
            )
            errors.append(error)

        return TaskResult(description=f"Check hostname is {target}", errors=errors)
