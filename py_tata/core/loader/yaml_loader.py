import pathlib

import yaml
from yaml.parser import ParserError
from yaml.reader import ReaderError
from yaml.scanner import ScannerError

from .exceptions import InvalidTasksDescription


class YamlLoader:
    def load(self, path: pathlib.Path) -> dict:
        try:
            with path.open("r") as file:
                content = yaml.full_load(file)
        except (ScannerError, ParserError, ReaderError):
            raise InvalidTasksDescription()
        return content
