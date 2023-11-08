import platform

from py_tata.tasks.task_result import TaskResult


class CheckHostnameTask:
    def __init__(self, target_hostname: str):
        self.target_hostname = target_hostname

    async def check(self) -> TaskResult:
        errors = []
        hostname = platform.node()
        if hostname != self.target_hostname:
            error = (
                f"Incorrect hostname: "
                f"Expected {self.target_hostname} but hostname is {hostname} now"
            )
            errors.append(error)

        return TaskResult(
            description=f"Check hostname is {self.target_hostname}",
            errors=errors,
        )
