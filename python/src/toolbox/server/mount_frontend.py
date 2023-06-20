from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def mount_frontend(app: FastAPI, react_build_dir: Path):
    app.mount("/", StaticFiles(directory=react_build_dir, html=True), name="static")
    app.mount(
        "/static", StaticFiles(directory=(react_build_dir / "static")), name="static"
    )
    return app
