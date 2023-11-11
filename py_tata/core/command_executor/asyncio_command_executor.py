import asyncio
import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class CommandResult:
    return_code: int
    stdout: str
    stderr: str


class AsyncioCommandExecutor:
    async def execute(self, *command):
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        return CommandResult(
            return_code=process.returncode,
            stdout=stdout.decode().strip(),
            stderr=stderr.decode().strip(),
        )
