from icmplib import async_ping

from py_tata.tasks import TaskResult


class CheckPingTask:
    def __init__(self, target_ip: str):
        self.target_ip = target_ip

    async def check(self) -> TaskResult:
        host = await async_ping(self.target_ip, count=3, privileged=False)
        errors = []
        if not host.is_alive:
            errors.append(f"Cannot ping host with ip={self.target_ip}")
        return TaskResult(
            description=f"Check ping for ip={self.target_ip}",
            errors=errors,
        )
