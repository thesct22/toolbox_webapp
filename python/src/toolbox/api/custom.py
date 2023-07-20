"""API endpoints for running custom playbooks."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from toolbox.core.ansible import Ansible
from toolbox.core.file import CustomFiles
from toolbox.core.rsakey import RSAKey


def custom_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/custom endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.get("/api/custom/playbooks", response_model=list)
    async def get_custom_playbooks() -> str:
        """
        Get the custom playbooks.

        Format:
        [
            {
                "is_file": true,
                "path": "path/to/ansible/playbook1",
                "name": "playbook1"
            },
            ...
        ]
        """
        try:
            root = CustomFiles(Path(__file__).parent.parent / "ansible")
            items = root.get_playbooks()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return jsonable_encoder(items)

    @app.get("/api/custom/inventories", response_model=list)
    async def get_custom_inventory() -> str:
        """
        Get the custom inventory.

        Format:
        {
            "is_file": false,
            "path": "path/to/ansible/inventory/group1",
            "name": "group1",
            "items": [
                {
                    "is_file": true,
                    "path": "path/to/ansible/inventory/group1/hosts1",
                    "name": "hosts1"
                },
                ...
            ]
        }
        """
        try:
            root = CustomFiles(Path(__file__).parent.parent / "ansible")
            items = root.get_inventory()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return jsonable_encoder(items)

    @app.put("/api/custom/run", response_model=str)
    async def run_custom(request: Request) -> str:
        """
        Run a custom playbook.

        Input Format:
        {
            "hosts": "hosts",
            "user": "user",
            "password": "password",
            "playbook": "playbook"
        }
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if (
            data["hosts"] == ""
            or data["user"] == ""
            or data["password"] == ""
            or data["playbook"] == ""
        ):
            raise HTTPException(
                status_code=400, detail="Missing hosts, user, password or playbook."
            )
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
            playbook = RSAKey().decrypt(data["playbook"])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=str(
                    "Missing hosts, user, password or playbook, or malformed data."
                ),
            )
        if hosts == "" or user == "" or password == "" or playbook == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user, password or playbook."
            )
        ansible = Ansible(
            inventory=hosts,
            user=user,
            password=password,
            playbook=playbook,
        )
        try:
            ansible.verfiy_auth()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        install_command = ansible.get_command()
        result = ansible.run_command(install_command)
        return result

    return app
