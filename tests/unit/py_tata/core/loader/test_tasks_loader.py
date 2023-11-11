import dataclasses
from pathlib import Path

import pydantic
import pytest

from py_tata.core.loader import InvalidTasksDescription, YamlLoader


@dataclasses.dataclass(frozen=True, slots=True)
class TaskMock:
    target: str


class TaskValidationModelMock(pydantic.BaseModel):
    target: str


class TestTasksLoader:
    def setup_method(self):
        self.sut = YamlLoader()
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

        result = self.sut.load(self.yaml_path)

        assert result == {
            "tasks": [
                {
                    "task": "check_hostname",
                    "target": "test-hostname",
                },
            ]
        }

    def test_load_raw_invalid_yaml(self):
        with self.yaml_path.open("w") as file:
            file.write("123: False: 123")

        with pytest.raises(InvalidTasksDescription):
            self.sut.load(self.yaml_path)
