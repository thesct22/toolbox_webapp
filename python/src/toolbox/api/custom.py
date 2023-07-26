"""API endpoints for running custom playbooks."""

import json
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
            verbosity = int(data["verbosity"])
        except ValueError:
            verbosity = 0
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
            playbook = RSAKey().decrypt(data["playbook"])
            extra_vars = RSAKey().decrypt(data["extra_vars"])
            tags = RSAKey().decrypt(data["tags"])
            extra_args = RSAKey().decrypt(data["extra_args"])
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
        try:
            extra_vars_temp = json.loads(extra_vars)
            extra_vars = []
            for item in extra_vars_temp:
                extra_vars_item = {item["key"]: item["value"]}
                extra_vars.append(extra_vars_item)
            tags = tags.split(",")
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400,
                detail=str("Malformed extra_vars, must be a JSON string."),
            )
        ansible = Ansible(
            inventory=hosts,
            user=user,
            password=password,
            playbook=playbook,
            extra_vars=extra_vars,
            verbosity=verbosity,
            tags=tags,
            extra_args=extra_args,
        )
        try:
            ansible.verfiy_auth()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        install_command = ansible.get_command()
        try:
            result = ansible.run_command(install_command)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return result

    return app
