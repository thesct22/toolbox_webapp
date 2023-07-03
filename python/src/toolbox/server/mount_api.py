"""API endpoints for the toolbox server."""
from typing import Dict

from fastapi import FastAPI
from toolbox.api.editor import editor_endpoints
from toolbox.api.install import install_endpoints
from toolbox.api.target import target_endpoints
from toolbox.api.uninstall import uninstall_endpoints
from toolbox.core.rsakey import RSAKey


def mount_api(app: FastAPI) -> FastAPI:
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

    @app.get("/api/public_key", response_model=Dict[str, str])
    def get_public_key() -> Dict[str, str]:
        """Return the public key."""
        public_key = RSAKey().get_public_key()
        return {"public_key": public_key}

    install_endpoint = install_endpoints(app)
    app.mount("/api/install", install_endpoint, name="install")

    uninstall_endpoint = uninstall_endpoints(app)
    app.mount("/api/uninstall", uninstall_endpoint, name="uninstall")

    target_endpoint = target_endpoints(app)
    app.mount("/api/target", target_endpoint, name="target")

    editor_endpoint = editor_endpoints(app)
    app.mount("/api/editor", editor_endpoint, name="editor")

    return app
