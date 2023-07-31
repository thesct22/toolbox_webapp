"""Run the server."""
import argparse
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolbox.server.main import run_server
from toolbox.server.mount_api import mount_api
from toolbox.server.mount_frontend import mount_frontend

app = FastAPI(title="Toolbox Webapp")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app = mount_api(app)
app = mount_frontend(app, react_build_dir=Path(__file__).parent / "build")

if __name__ == "__main__":
    """Run the server."""
    parser = argparse.ArgumentParser(description="Run the server.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to run the server on.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on.",
    )
    args = parser.parse_args()

    run_server(app=app, host=args.host, port=args.port)
