from fastapi import FastAPI
from pathlib import Path
import uvicorn

from toolbox.server.mount_api import mount_api
from toolbox.server.mount_frontend import mount_frontend

def run_server(
        react_build_dir: Path = Path(__file__).parent.parent / "build",
        host: str = "localhost",
        port: int = 8000,
    ):
    app = FastAPI(title="Toolbox Webapp")
    app = mount_api(app)
    app = mount_frontend(app, react_build_dir=react_build_dir)

    uvicorn.run(app, host=host, port=port)
