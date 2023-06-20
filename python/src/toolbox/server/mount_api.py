"""API endpoints for the toolbox server."""

from fastapi import FastAPI


def mount_api(app: FastAPI):
    """
    Mount the API endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api")
    def read_root():
        """Return a hello world message."""
        return {"Hello": "World"}

    @app.get("/api/items/{item_id}")
    def read_item(item_id: int, q: str = ""):
        """Return the item id and query string."""
        return {"item_id": item_id, "q": q}

    return app
