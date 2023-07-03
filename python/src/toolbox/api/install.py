"""Install API endpoints."""

from typing import Dict, List

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from toolbox.core.tags import InstallationTags


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
        return response

    return app
