import asyncio
from pathlib import Path

import typer
from rich import print as rich_print
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)
from typer import Typer

from py_tata.builder import TaskBuilder
from py_tata.loader import TasksLoader
from py_tata.runner import Runner
from py_tata.tasks.check_hostname import CheckHostnameIn, CheckHostnameTask
from py_tata.tasks.check_ping import CheckPingIn, CheckPingTask

app = Typer()


@app.command()
def main(tasks_path: Path):
    try:
        asyncio.run(async_main(tasks_path))
    except Exception as e:
        exception_type = type(e).__name__
        error_message = str(e)
        formatted_exception = f"[bold red]{exception_type}:[/] {error_message}"
        rich_print(formatted_exception)
        raise typer.Exit(1)


async def async_main(tasks_path: Path):
    rich_print(f"[cyan]Collecting tasks...[/]")
    loader = TasksLoader(
        task_name_to_builder={
            "check_hostname": TaskBuilder(
                validation_model=CheckHostnameIn,
                task_class=CheckHostnameTask,
            ),
            "check_ping": TaskBuilder(
                validation_model=CheckPingIn,
                task_class=CheckPingTask,
            ),
        }
    )
    tasks = loader.load(tasks_path)
    rich_print(f"[bold cyan]{len(tasks)} tasks collected[/]")
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


if __name__ == "__main__":
    app()
