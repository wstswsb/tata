from typing import Literal

from pydantic import BaseModel


class LinuxCheckIPv4ForwardingIn(BaseModel):
    task: Literal["linux_check_ipv4_forwarding"]
    enabled: bool
