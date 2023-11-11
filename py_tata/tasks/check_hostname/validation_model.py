from typing import Literal

from pydantic import BaseModel, ConfigDict


class CheckHostnameIn(BaseModel):
    task: Literal["check_hostname"]
    target_hostname: str

    model_config = ConfigDict(extra="forbid")
