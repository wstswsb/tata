from ..task_abc import LinuxCheckIpForwardingTask


class LinuxCheckIPv4ForwardingTask(LinuxCheckIpForwardingTask):
    @property
    def status_check_command(self) -> tuple[str, ...]:
        return "sysctl", "-n", "net.ipv4.ip_forward"

    @property
    def ip_version(self) -> str:
        return "IPv4"
