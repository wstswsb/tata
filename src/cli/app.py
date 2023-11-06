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
    loader = TasksLoader(
        task_name_to_class={
            "check_hostname": CheckHostnameTask,
            "check_ping": CheckPingTask,
        }
    )
    runner = Runner(tasks=loader.load(tasks_path))
    results = asyncio.run(runner.run())
    rich_print(results)


if __name__ == "__main__":
    app()
