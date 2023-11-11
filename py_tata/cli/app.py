import asyncio
from pathlib import Path
from typing import Any

import typer
from pydantic import ValidationError
from rich import print as rich_print
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)
from typer import Typer

import py_tata.tasks.check_hostname as check_hostname
import py_tata.tasks.check_ping as check_ping
import py_tata.tasks.linux_check_ipv4_forwarding as linux_check_ipv4_forwarding
from py_tata.core.builder.task_builder import TaskBuilder
from py_tata.core.loader import YamlLoader
from py_tata.core.loader.exceptions import InvalidTasksDescription
from py_tata.core.runner import Runner
from py_tata.tasks.validation_model import TasksContainer

_task_name_to_builder: dict[str, TaskBuilder] = {
    **check_hostname.TASK_NAME_TO_BUILDER,
    **check_ping.TASK_NAME_TO_BUILDER,
    **linux_check_ipv4_forwarding.TASK_NAME_TO_BUILDER,
}

app = Typer()


@app.command()
def main(tasks_path: Path):
    asyncio.run(async_main(tasks_path))


async def async_main(tasks_path: Path):
    rich_print(f"[cyan]Collecting tasks...[/]")
    raw_content = __load_yaml(tasks_path)
    tasks_container = __build_tasks_container(raw_content)
    tasks = __build_tasks(tasks_container)
    rich_print(f"[bold cyan]{len(tasks_container.tasks)} tasks collected[/]")
    runner = Runner(tasks)

    progress_bar = Progress(
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    )
    with progress_bar as progress:
        task = progress.add_task(description="", total=len(tasks))
        for index, completed_coro in enumerate(runner.run()):
            result = await completed_coro
            if not result.errors:
                rich_print(f"[green][+] Task {result.description}[/]")
            else:
                rich_print(
                    f"[red][-] Task {result.description}\t| {','.join(result.errors)}[/]"
                )
            progress.update(task, completed=index + 1)


def __load_yaml(tasks_path: Path) -> dict:
    try:
        raw_tasks_container = YamlLoader().load(tasks_path)
    except InvalidTasksDescription:
        rich_print(f"[red]Invalid yaml: {tasks_path}[/]")
        raise typer.Exit(1)
    return raw_tasks_container


def __build_tasks_container(raw_yaml: Any) -> TasksContainer:
    try:
        tasks_container = TasksContainer.model_validate(raw_yaml)
    except ValidationError as e:
        rich_print("[bold red]Validation error:[/]")
        rich_print(e)
        raise typer.Exit(1)
    return tasks_container


def __build_tasks(tasks_container: TasksContainer) -> list:
    return [
        _task_name_to_builder[task_in.task].build(task_in)
        for task_in in tasks_container.tasks
    ]


if __name__ == "__main__":
    app()
