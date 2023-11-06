import asyncio
from pathlib import Path

from rich import print as rich_print
from typer import Typer

from src.tasks.check_hostname import CheckHostnameTask
from src.tasks.check_ping import CheckPingTask
from src.tasks.loader import TasksLoader
from src.tasks.runner import Runner

app = Typer()


@app.command()
def main(tasks_path: Path):
    asyncio.run(async_main(tasks_path))


async def async_main(tasks_path: Path):
    loader = TasksLoader(
        task_name_to_class={
            "check_hostname": CheckHostnameTask,
            "check_ping": CheckPingTask,
        }
    )
    runner = Runner(tasks=loader.load(tasks_path))
    for completed_coro in runner.run():
        result = await completed_coro
        if not result.errors:
            rich_print(f"[green][+] Task {result.description}[/]")
        else:
            rich_print(f"[red][-] Task {result.description} {result.errors}[/]")


if __name__ == "__main__":
    app()
