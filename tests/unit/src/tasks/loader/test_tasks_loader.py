import dataclasses
from pathlib import Path

import pytest

from src.tasks.loader import InvalidTasksDescription, TasksLoader
from src.tasks.loader.exceptions import InvalidTaskName


@dataclasses.dataclass(frozen=True, slots=True)
class TaskMock:
    target: str


class TestTasksLoader:
    def setup_method(self):
        self.sut = TasksLoader(task_name_to_class={"task_mock": TaskMock})
        self.yaml_path = Path("tests/unit/files/test_tasks_loader.yaml")

    def teardown_method(self):
        self.yaml_path.unlink(missing_ok=True)

    def test_load_raw_valid_yaml(self):
        with self.yaml_path.open("w") as file:
            file.write(
                "\n".join(
                    (
                        "tasks:",
                        "  - task: check_hostname",
                        "    target: test-hostname",
                    )
                )
            )

        result = self.sut._load_raw(self.yaml_path)

        assert result == [
            {
                "task": "check_hostname",
                "target": "test-hostname",
            },
        ]

    def test_load_raw_invalid_yaml(self):
        with self.yaml_path.open("w") as file:
            file.write("123: False: 123")

        with pytest.raises(InvalidTasksDescription):
            self.sut._load_raw(self.yaml_path)

    def test_load_tasks_success(self):
        with self.yaml_path.open("w") as file:
            file.write(
                "\n".join(
                    (
                        "tasks:",
                        "  - task: task_mock",
                        "    target: target_mock",
                    )
                )
            )

        result = self.sut.load(self.yaml_path)

        assert result == [TaskMock("target_mock")]

    def test_load_tasks_invalid_task_name(self):
        with self.yaml_path.open("w") as file:
            file.write(
                "\n".join(
                    (
                        "tasks:",
                        "  - task: invalid_name",
                        "    target: target_mock",
                    )
                )
            )

        with pytest.raises(InvalidTaskName) as e:
            self.sut.load(self.yaml_path)

        assert e.value.args[0] == "No task for task_name='invalid_name'"
