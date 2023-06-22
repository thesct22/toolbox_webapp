"""Run the server."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolbox.server.mount_api import mount_api
from toolbox.server.mount_frontend import mount_frontend
import uvicorn


def run_server(
    react_build_dir: Path = Path(__file__).parent.parent / "build",
    host: str = "localhost",
    port: int = 8000,
):
    """
    Run the server.

    Args:
        react_build_dir (Path): Path to the react build directory.
        host (str): Host to run the server on.
        port (int): Port to run the server on.
    """
    app = FastAPI(title="Toolbox Webapp")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app = mount_api(app)
    app = mount_frontend(app, react_build_dir=react_build_dir)

    uvicorn.run(app, host=host, port=port)
