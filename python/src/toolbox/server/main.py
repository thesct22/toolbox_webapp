"""Run the server."""
from fastapi import FastAPI
import uvicorn


def run_server(
    app: FastAPI,
    host: str = "localhost",
    port: int = 8000,
):
    """
    Run the server.

    Args:
        app (FastAPI): FastAPI app.
        host (str): Host to run the server on.
        port (int): Port to run the server on.
    """
    uvicorn.run(app, host=host, port=port)
