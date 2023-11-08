from typer.testing import CliRunner

from py_tata.cli.app import app


class TestApp:
    def setup_method(self):
        self.sut = CliRunner()

    def test_call(self):
        result = self.sut.invoke(
            app,
            ["--tasks_path=./tests/integration/files/tasks.yaml"],
        )
