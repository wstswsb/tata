from typing import TypeVar

import pydantic

T = TypeVar("T")


class TaskBuilder:
    def __init__(self, task_class: T):
        self.task_class = task_class

    def build(self, model_in: pydantic.BaseModel) -> T:
        return self.task_class(**model_in.model_dump())
