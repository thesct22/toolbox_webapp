"""File editor API endpoints."""

from pathlib import Path
from typing import Dict, List, Union

from fastapi import FastAPI, HTTPException, Request
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
    async def write_file(request: Request) -> Dict[str, str]:
        """
        Write a file.

        Args:
            request (Request): The request.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "" or data["content"] == "":
            raise HTTPException(status_code=400, detail="Missing path or content.")
        path = data["path"]
        content = data["content"]
        try:
            file = File(path)
            written = file.write_content(content)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"written": str(written), "success": "true"}

    @app.post("/api/editor/file/create", response_model=Dict[str, str])
    async def create_file(request: Request) -> Dict[str, str]:
        """
        Create a file.

        Args:
            path (str): The path of the file to create.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "":
            raise HTTPException(status_code=400, detail="Missing path.")
        path = data["path"]
        try:
            file = File(path)
            file.create()
        except ValueError as e:
            message = str(e).split("\n")[2].strip()
            message = message.split("(")[0].strip()
            raise HTTPException(status_code=404, detail=message)
        except FileExistsError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"created": "true"}

    @app.post("/api/editor/file/delete", response_model=Dict[str, str])
    async def delete_file(request: Request) -> Dict[str, str]:
        """
        Delete a file.

        Args:
            request (Request): The request.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "":
            raise HTTPException(status_code=400, detail="Missing path.")
        path = data["path"]
        try:
            file = File(path)
            file.delete()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"deleted": "true"}

    @app.post("/api/editor/file/rename", response_model=Dict[str, str])
    async def rename_file(request: Request) -> Dict[str, str]:
        """
        Rename a file.

        Args:
            request (Request): The request.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "" or data["new_path"] == "":
            raise HTTPException(status_code=400, detail="Missing path or new_path.")
        path = data["path"]
        new_path = data["new_path"]
        try:
            file = File(path)
            new_name = file.rename(new_path)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"new_path": new_name.as_posix()}

    @app.post("/api/editor/folder/create", response_model=Dict[str, str])
    async def create_folder(request: Request) -> Dict[str, str]:
        """
        Create a folder.

        Args:
            path (str): The path of the folder to create.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "":
            raise HTTPException(status_code=400, detail="Missing path.")
        path = data["path"]
        try:
            folder = Folder(path)
            folder.create()
        except ValueError as e:
            message = str(e).split("\n")[2].strip()
            message = message.split("(")[0].strip()
            raise HTTPException(status_code=404, detail=message)
        except FileExistsError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"created": "true"}

    @app.post("/api/editor/folder/delete", response_model=Dict[str, str])
    async def delete_folder(request: Request) -> Dict[str, str]:
        """
        Delete a folder.

        Args:
            path (str): The path of the folder to delete.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "":
            raise HTTPException(status_code=400, detail="Missing path.")
        path = data["path"]
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
    async def delete_folder_confirmed(request: Request) -> Dict[str, str]:
        """
        Delete a folder.

        Args:
            request (Request): The request.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "":
            raise HTTPException(status_code=400, detail="Missing path.")
        path = data["path"]
        try:
            folder = Folder(path)
            folder.force_delete()
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"deleted": "true"}

    @app.post("/api/editor/folder/rename", response_model=Dict[str, str])
    async def rename_folder(request: Request) -> Dict[str, str]:
        """
        Rename a folder.

        Args:
            request (Request): The request.
        Returns:
            Dict[str, str]: The file content.
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["path"] == "" or data["new_path"] == "":
            raise HTTPException(status_code=400, detail="Missing path or new_path.")
        path = data["path"]
        new_path = data["new_path"]
        try:
            folder = Folder(path)
            new_name = folder.rename(new_path)
        except ValueError or FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"new_path": new_name.as_posix()}

    return app
