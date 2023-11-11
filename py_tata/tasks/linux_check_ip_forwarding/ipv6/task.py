from ..task_abc import LinuxCheckIpForwardingTask


class LinuxCheckIPv6ForwardingTask(LinuxCheckIpForwardingTask):
    @property
    def status_check_command(self) -> tuple[str, ...]:
        return "sysctl", "-n", "net.ipv6.conf.all.forwarding"

    @property
    def ip_version(self) -> str:
        return "IPv6"
