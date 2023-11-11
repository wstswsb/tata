from typing import Literal

from pydantic import BaseModel


class LinuxCheckIPv6ForwardingIn(BaseModel):
    task: Literal["linux_check_ipv6_forwarding"]
    enabled: bool
