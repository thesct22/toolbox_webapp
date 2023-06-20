"""Mount the frontend static files to the FastAPI app."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def mount_frontend(app: FastAPI, react_build_dir: Path):
    """
    Mount the frontend static files to the FastAPI app.

    Args:
        app (FastAPI): The FastAPI app.
        react_build_dir (Path): Path to the react build directory.
    Returns:
        FastAPI: The FastAPI app.
    """
    app.mount("/", StaticFiles(directory=react_build_dir, html=True), name="static")
    app.mount(
        "/static", StaticFiles(directory=(react_build_dir / "static")), name="static"
    )
    return app
