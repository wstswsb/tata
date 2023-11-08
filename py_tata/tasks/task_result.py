import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class TaskResult:
    description: str
    errors: list[str]
