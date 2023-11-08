import pathlib

import yaml
from yaml.scanner import ScannerError

from .exceptions import InvalidTaskName, InvalidTasksDescription


class TasksLoader:
    def __init__(self, task_name_to_class: dict[str, type]):
        self._task_name_to_class = task_name_to_class

    def load(self, tasks_store: pathlib.Path) -> list:
        tasks = []
        for raw_task in self._load_raw(tasks_store):
            task_name = raw_task.pop("task")
            task_class = self._task_name_to_class.get(task_name)
            if not task_class:
                raise InvalidTaskName(f"No task for {task_name=}")
            tasks.append(task_class(**raw_task))
        return tasks

    def _load_raw(self, tasks_store: pathlib.Path) -> list[dict]:
        try:
            with tasks_store.open("r") as file:
                content = yaml.full_load(file)
        except ScannerError:
            raise InvalidTasksDescription()
        return content.get("tasks", [])
