from typing import Type, TypeVar

import pydantic

T = TypeVar("T")


class TaskBuilder:
    def __init__(self, validation_model: Type[pydantic.BaseModel], task_class: T):
        self.validation_model = validation_model
        self.task_class = task_class

    def build(self, attrs: dict) -> T:
        model_in = self.validation_model(**attrs)
        return self.task_class(**model_in.model_dump())
