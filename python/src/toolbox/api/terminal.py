"""APIs for implementing a websocket terminal."""

from fastapi import FastAPI, WebSocket
from toolbox.core.terminal import TerminalModel


def terminal_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/terminal endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.websocket("/api/terminal")
    async def terminal(websocket: WebSocket) -> None:
        """Run a terminal."""
        await websocket.accept()
        terminal = TerminalModel(websocket=websocket)
        await terminal.run()

    return app
