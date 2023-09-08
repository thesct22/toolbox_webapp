"""API endpoints for the toolbox server."""
from typing import Dict

from fastapi import FastAPI
from toolbox.api.custom import custom_endpoints
from toolbox.api.editor import editor_endpoints
from toolbox.api.install import install_endpoints
from toolbox.api.target import target_endpoints
from toolbox.api.uninstall import uninstall_endpoints
from toolbox.core.rsakey import RSAKey


def mount_api(
    app: FastAPI, terminal_host: str = "localhost", terminal_port: int = 8765
) -> FastAPI:
    """
    Mount the API endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api")
    def read_root() -> str:
        """Return a hello world message."""
        return "This is the toolbox server API endpoint."

    @app.get("/api/health")
    def read_health() -> str:
        """Return a health message."""
        return "OK"

    @app.get("/api/public_key", response_model=Dict[str, str])
    def get_public_key() -> Dict[str, str]:
        """Return the public key."""
        public_key = RSAKey().get_public_key()
        return {"public_key": public_key}

    @app.get("/api/terminal/url", response_model=Dict[str, str])
    def get_terminal_url() -> Dict[str, str]:
        """Return the terminal url."""
        return {"host": terminal_host, "port": terminal_port}

    install_endpoint = install_endpoints(app)
    app.mount("/api/install", install_endpoint, name="install")

    uninstall_endpoint = uninstall_endpoints(app)
    app.mount("/api/uninstall", uninstall_endpoint, name="uninstall")

    target_endpoint = target_endpoints(app)
    app.mount("/api/target", target_endpoint, name="target")

    editor_endpoint = editor_endpoints(app)
    app.mount("/api/editor", editor_endpoint, name="editor")

    custom_endpoint = custom_endpoints(app)
    app.mount("/api/custom", custom_endpoint, name="custom")

    return app
