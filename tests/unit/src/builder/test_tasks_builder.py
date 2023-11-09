import pydantic

from py_tata.builder import TaskBuilder


class TaskClassMock:
    def __init__(self, target_test_argument_1, target_test_argument_2):
        self.target_test_argument_1 = target_test_argument_1
        self.target_test_argument_2 = target_test_argument_2


class ValidationModelMock(pydantic.BaseModel):
    target_test_argument_1: str
    target_test_argument_2: int


class TestTaskBuilder:
    def setup_method(self):
        self.sut = TaskBuilder(
            validation_model=ValidationModelMock,
            task_class=TaskClassMock,
        )

    def test_build(self):
        attrs = {
            "target_test_argument_1": "test_arg_1",
            "target_test_argument_2": 1,
        }

        result = self.sut.build(attrs)

        assert isinstance(result, TaskClassMock)
        assert result.target_test_argument_1 == attrs["target_test_argument_1"]
        assert result.target_test_argument_2 == attrs["target_test_argument_2"]
