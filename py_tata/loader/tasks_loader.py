import pathlib

import yaml
from yaml.scanner import ScannerError

from py_tata.builder import TaskBuilder

from .exceptions import InvalidTaskName, InvalidTasksDescription


class TasksLoader:
    def __init__(self, task_name_to_builder: dict[str, TaskBuilder]):
        self._task_name_to_builder = task_name_to_builder

    def load(self, tasks_store: pathlib.Path) -> list:
        tasks = []
        for raw_task in self._load_raw(tasks_store):
            task_name = raw_task.pop("task")
            task_builder = self._task_name_to_builder.get(task_name)
            if not task_builder:
                raise InvalidTaskName(f"No task for {task_name=}")
            tasks.append(task_builder.build(raw_task))
        return tasks

    def _load_raw(self, tasks_store: pathlib.Path) -> list[dict]:
        try:
            with tasks_store.open("r") as file:
                content = yaml.full_load(file)
        except ScannerError:
            raise InvalidTasksDescription()
        return content.get("tasks", [])
