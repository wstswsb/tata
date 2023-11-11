import pydantic

from py_tata.core.builder.task_builder import TaskBuilder


class TaskClassMock:
    def __init__(self, target_test_argument_1, target_test_argument_2):
        self.target_test_argument_1 = target_test_argument_1
        self.target_test_argument_2 = target_test_argument_2


class ValidationModelMock(pydantic.BaseModel):
    target_test_argument_1: str
    target_test_argument_2: int


class TestTaskBuilder:
    def setup_method(self):
        self.sut = TaskBuilder(task_class=TaskClassMock)

    def test_build(self):
        model_in = ValidationModelMock(
            target_test_argument_1="string",
            target_test_argument_2=123,
        )
        result = self.sut.build(model_in)

        assert isinstance(result, TaskClassMock)
        assert result.target_test_argument_1 == model_in.target_test_argument_1
        assert result.target_test_argument_2 == model_in.target_test_argument_2
