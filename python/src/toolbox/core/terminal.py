"""A class that runs a terminal on server and connects from client using websocket."""

from pathlib import Path
import subprocess

from fastapi import WebSocket
from pydantic import BaseModel, Field, validator


class TerminalModel(BaseModel):
    """The terminal model."""

    command: str = Field(
        "bash",
        description="The command to run.",
    )
    cwd: Path = Field(
        Path(__file__).parent.parent,
        description="The current working directory.",
    )
    timeout: int = Field(
        10,
        description="The timeout for the command.",
    )
    websocket: WebSocket = Field(
        ...,
        description="The websocket connection.",
    )

    def __init__(self, **data):
        """Initialize the terminal model."""
        super().__init__(**data)
        if "command" in data:
            self.command = data["command"]
        if "cwd" in data:
            self.cwd = data["cwd"]
        if "timeout" in data:
            self.timeout = data["timeout"]
        if "websocket" in data:
            self.websocket = data["websocket"]

    @validator("cwd", pre=True)
    def cwd_path(cls, v):
        """Validate the cwd."""
        if isinstance(v, str):
            return Path(v)
        return v

    @validator("timeout", pre=True)
    def timeout_int(cls, v):
        """Validate the timeout."""
        if isinstance(v, str):
            return int(v)
        return v

    async def run(self) -> None:
        """Run the command."""
        await self.websocket.accept()

        self.command = await self.websocket.receive_text()
        proc = subprocess.Popen(
            self.command,
            cwd=self.cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        try:
            outs, errs = proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        await self.websocket.send_text(outs.decode("utf-8"))
        await self.websocket.send_text(errs.decode("utf-8"))
        # return outs, errs

    def run_async(self) -> subprocess.Popen:
        """Run the command async."""
        proc = subprocess.Popen(
            self.command,
            cwd=self.cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        return proc

    def run_async_read(self, proc: subprocess.Popen) -> tuple:
        """Run the command async and read output."""
        outs, errs = proc.communicate()
        return outs, errs
