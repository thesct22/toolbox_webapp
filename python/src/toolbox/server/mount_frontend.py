from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path


def mount_frontend(app: FastAPI, react_build_dir: Path)-> FastAPI:

    @app.get("/custom-playbook")
    async def custom_playbook(request: Request):
        return FileResponse(react_build_dir / "index.html")
    
    @app.get("/configure-target")
    async def configure_target(request: Request):
        return FileResponse(react_build_dir / "index.html")
    
    @app.get("/code-editor")
    async def code_editor(request: Request):
        return FileResponse(react_build_dir / "index.html")
    
    @app.get("/terminal")
    async def terminal(request: Request):
        return FileResponse(react_build_dir / "index.html")
    
    @app.get("/instructions")
    async def instructions(request: Request):
        return FileResponse(react_build_dir / "index.html")

    app.mount("/", StaticFiles(directory=react_build_dir, html=True), name="static")
    
    return app