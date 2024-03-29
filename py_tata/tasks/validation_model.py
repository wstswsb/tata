from collections import Counter
from typing import get_args

from pydantic import BaseModel, field_validator

from py_tata.tasks.check_hostname.validation_model import CheckHostnameIn
from py_tata.tasks.check_ping.validation_model import CheckPingIn
from py_tata.tasks.linux_check_ip_forwarding.ipv4 import LinuxCheckIPv4ForwardingIn
from py_tata.tasks.linux_check_ip_forwarding.ipv6 import LinuxCheckIPv6ForwardingIn

_unique_types = (
    CheckHostnameIn,
    LinuxCheckIPv4ForwardingIn,
    LinuxCheckIPv6ForwardingIn,
)
_validation_tasks_types = (
    CheckHostnameIn
    | CheckPingIn
    | LinuxCheckIPv4ForwardingIn
    | LinuxCheckIPv6ForwardingIn
)


class TasksContainer(BaseModel):
    tasks: list[_validation_tasks_types]

    @field_validator("tasks")
    @classmethod
    def check_unique_tasks(cls, v: list):
        type_counts = Counter(type(x) for x in v)
        error_tasks = []
        for unique_type in _unique_types:
            if type_counts[unique_type] < 2:
                continue
            task_name = get_args(unique_type.__annotations__["task"])[0]
            error_tasks.append(f"'{task_name}'")
        if error_tasks:
            raise ValueError(", ".join(error_tasks) + " can be used only once")
        return v
