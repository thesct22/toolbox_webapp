"""Mounts the frontend to the server."""
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def mount_frontend(app: FastAPI, react_build_dir: Path) -> FastAPI:
    """
    Mounts the frontend to the server.

    Args:
        app (FastAPI): The FastAPI instance.
        react_build_dir (Path): The path to the react build directory.
    Returns:
        FastAPI: The FastAPI instance.
    """

    @app.get("/custom-playbook")
    async def custom_playbook(request: Request):
        """Serve the index.html file for the custom playbook page."""
        return FileResponse(react_build_dir / "index.html")

    @app.get("/configure-target")
    async def configure_target(request: Request):
        """Serve the index.html file for the configure target page."""
        return FileResponse(react_build_dir / "index.html")

    @app.get("/code-editor")
    async def code_editor(request: Request):
        """Serve the index.html file for the code editor page."""
        return FileResponse(react_build_dir / "index.html")

    @app.get("/terminal")
    async def terminal(request: Request):
        """Serve the index.html file for the terminal page."""
        return FileResponse(react_build_dir / "index.html")

    @app.get("/instructions")
    async def instructions(request: Request):
        """Serve the index.html file for the instructions page."""
        return FileResponse(react_build_dir / "index.html")

    app.mount("/", StaticFiles(directory=react_build_dir, html=True), name="static")

    return app
