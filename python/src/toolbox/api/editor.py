"""File editor API endpoints."""

from pathlib import Path
from typing import Dict, List, Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from toolbox.core.file import AnsibleRootFolder, File, Folder


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
        try:
            root = AnsibleRootFolder(Path(__file__).parent.parent / "ansible")
            items = root.get_items()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
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
        try:
            file = File(path)
            content = file.read_content()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
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
        try:
            file = File(path)
            written = file.write_content(content)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"written": str(written)}

    @app.post("/api/editor/file/create", response_model=Dict[str, str])
    def create_file(path: str) -> Dict[str, str]:
        """
        Create a file.

        Args:
            path (str): The path of the file to create.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            file = File(path)
            file.create()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"created": "true"}

    @app.post("/api/editor/file/delete", response_model=Dict[str, str])
    def delete_file(path: str) -> Dict[str, str]:
        """
        Delete a file.

        Args:
            path (str): The path of the file to delete.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            file = File(path)
            file.delete()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"deleted": "true"}

    @app.post("/api/editor/file/rename", response_model=Dict[str, str])
    def rename_file(path: str, new_path: str) -> Dict[str, str]:
        """
        Rename a file.

        Args:
            path (str): The path of the file to rename.
            new_path (str): The new path of the file.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            file = File(path)
            new_name = file.rename(new_path)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"new_path": new_name.as_posix()}

    @app.post("/api/editor/folder/create", response_model=Dict[str, str])
    def create_folder(path: str) -> Dict[str, str]:
        """
        Create a folder.

        Args:
            path (str): The path of the folder to create.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            folder = Folder(path)
            folder.create()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"created": "true"}

    @app.post("/api/editor/folder/delete", response_model=Dict[str, str])
    def delete_folder(path: str) -> Dict[str, str]:
        """
        Delete a folder.

        Args:
            path (str): The path of the folder to delete.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            folder = Folder(path)
            folder.delete()
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValueError as e:
            if "is not empty" in str(e):
                return {"deleted": "get_confirmation"}
        return {"deleted": "true"}

    @app.post("/api/editor/folder/delete/confirmed", response_model=Dict[str, str])
    def delete_folder_confirmed(path: str) -> Dict[str, str]:
        """
        Delete a folder.

        Args:
            path (str): The path of the folder to delete.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            folder = Folder(path)
            folder.force_delete()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"deleted": "true"}

    @app.post("/api/editor/folder/rename", response_model=Dict[str, str])
    def rename_folder(path: str, new_path: str) -> Dict[str, str]:
        """
        Rename a folder.

        Args:
            path (str): The path of the folder to rename.
            new_path (str): The new path of the folder.
        Returns:
            Dict[str, str]: The file content.
        """
        try:
            folder = Folder(path)
            new_name = folder.rename(new_path)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"new_path": new_name.as_posix()}

    return app
