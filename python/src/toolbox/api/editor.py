"""File editor API endpoints."""

from pathlib import Path
from typing import Dict, List, Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from toolbox.core.file import AnsibleRootFolder, File


def editor_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/editor endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get(
        "/api/editor/files", response_model=List[Dict[str, Union[bool, str, list]]]
    )
    def get_files() -> List[Dict[str, Union[bool, str, list]]]:
        """
        Return all the files.

        Format:
        [
            {
                "is_file": true,
                "path": "path/to/file",
            },
            {
                "is_file": false,
                "path": "path/to/ansible/inventory",
                "items": [
                    {
                        "is_file": true,
                        "path": "path/to/ansible/inventory/file",
                    },
                    ...
                ]
            },
            ...
        ]
        """
        root = AnsibleRootFolder(Path(__file__).parent.parent / "ansible")
        items = root.get_items()
        return jsonable_encoder(items)

    @app.get("/api/editor/file/read", response_model=Dict[str, str])
    def read_file(path: str) -> Dict[str, str]:
        """
        Read a file.

        Args:
            path (str): The path of the file to read.
        Returns:
            Dict[str, str]: The file content.
        """
        file = File(path)
        content = file.read_content()
        return {"content": content}

    @app.post("/api/editor/file/write", response_model=Dict[str, str])
    def write_file(path: str, content: str) -> Dict[str, str]:
        """
        Write a file.

        Args:
            path (str): The path of the file to write.
            content (str): The content to write.
        Returns:
            Dict[str, str]: The file content.
        """
        file = File(path)
        file.write_content(content)
        return {"content": content}

    return app
