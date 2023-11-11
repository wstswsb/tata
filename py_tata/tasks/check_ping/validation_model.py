from typing import Literal

from pydantic import BaseModel


class CheckPingIn(BaseModel):
    task: Literal["check_ping"]
    target_ip: str
