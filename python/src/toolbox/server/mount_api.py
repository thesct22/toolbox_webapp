"""API endpoints for the toolbox server."""
from typing import Dict, List

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from toolbox.core.tags import InstallationTags, UninstallationTags


def mount_api(app: FastAPI) -> FastAPI:
    """
    Mount the API endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api")
    def read_root() -> Dict[str, str]:
        """Return a hello world message."""
        return {"Hello": "World"}

    @app.get("/api/items/{item_id}")
    def read_item(item_id: int, q: str = "") -> Dict[str, int | str]:
        """Return the item id and query string."""
        return {"item_id": item_id, "q": q}

    install_endpoint = install_endpoints(app)
    app.mount("/api/install", install_endpoint, name="install")

    uninstall_endpoint = uninstall_endpoints(app)
    app.mount("/api/uninstall", uninstall_endpoint, name="uninstall")

    return app


def install_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/install endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api/install/tags", response_model=List[Dict[str, str | List[str]]])
    def get_tags() -> List[Dict[str, str | List[str]]]:
        """
        Return all the tags.

        Format:
        [
            {
                "title": "software_name",
                "tags": ["tag1", "tag2", ...]
            },
            ...
        ]
        """
        tags = InstallationTags()
        tags.read_tags_from_playbooks()
        response = jsonable_encoder(tags.get_tags())
        print(response)
        return response

    return app


def uninstall_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/uninstall endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api/uninstall/tags", response_model=List[Dict[str, str | List[str]]])
    def get_tags() -> List[Dict[str, str | List[str]]]:
        """
        Return all the tags.

        Format:
        [
            {
                "title": "software_name",
                "tags": ["tag1", "tag2", ...]
            },
            ...
        ]
        """
        tags = UninstallationTags()
        tags.read_tags_from_playbooks()
        response = jsonable_encoder(tags.get_tags())
        return response

    return app
