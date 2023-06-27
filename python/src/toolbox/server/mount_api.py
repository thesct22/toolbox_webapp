"""API endpoints for the toolbox server."""
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from toolbox.core.ansible import Ansible
from toolbox.core.rsakey import RSAKey
from toolbox.core.tags import InstallationTags, UninstallationTags
from toolbox.helpers.config_target import config_target


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


def target_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/target endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.put("/api/target/configure", response_model=str)
    async def configure_target(request: Request) -> str:
        """
        Configure the target machines.

        Input Format:
        {
            "hosts": "hosts",
            "user": "user",
            "password": "password"
        }
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        hosts = RSAKey().decrypt(data["hosts"])
        user = RSAKey().decrypt(data["user"])
        password = RSAKey().decrypt(data["password"])
        hosts = hosts.split(",")
        for host in hosts:
            config_target(host, user, password)
        return "Configured target machines."

    @app.put("/api/target/ping", response_model=str)
    async def ping_target(request: Request) -> str:
        """
        Ping the target machines.

        Input Format:
        {
            "hosts": "hosts",
            "user": "user",
            "password": "password"
        }
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        print(data["hosts"])
        hosts = RSAKey().decrypt(data["hosts"])
        user = RSAKey().decrypt(data["user"])
        password = RSAKey().decrypt(data["password"])
        ansible = Ansible(inventory=hosts, user=user, password=password)
        try:
            ansible.verfiy_auth()
        except ValueError as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
        ping_command = ansible.get_ping_command()
        result = ansible.run_command(ping_command)
        return result

    @app.put("/api/target/install", response_model=str)
    async def install_target(request: Request) -> str:
        """
        Install the software on the target machines.

        Input Format:
        {
            "hosts": "hosts",
            "user": "user",
            "password": "password",
            "tags": ["tag1", "tag2", ...]
        }
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        if data["tags"] == []:
            raise HTTPException(status_code=400, detail="No tags provided.")
        hosts = RSAKey().decrypt(data["hosts"])
        user = RSAKey().decrypt(data["user"])
        password = RSAKey().decrypt(data["password"])
        tags = data.get("tags")
        ansible = Ansible(
            inventory=hosts,
            user=user,
            password=password,
            tags=tags,
            playbook="install.yml",
        )
        try:
            ansible.verfiy_auth()
        except ValueError as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
        install_command = ansible.get_command()
        result = ansible.run_command(install_command)
        return result

    @app.put("/api/target/uninstall", response_model=str)
    async def uninstall_target(request: Request) -> str:
        """
        Uninstall the software on the target machines.

        Input Format:
        {
            "hosts": "hosts",
            "user": "user",
            "password": "password",
            "tags": ["tag1", "tag2", ...]
        }
        """
        data = await request.json()
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        if data["tags"] == []:
            raise HTTPException(status_code=400, detail="No tags provided.")
        hosts = RSAKey().decrypt(data["hosts"])
        user = RSAKey().decrypt(data["user"])
        password = RSAKey().decrypt(data["password"])
        tags = data.get("tags")
        ansible = Ansible(
            inventory=hosts,
            user=user,
            password=password,
            tags=tags,
            playbook="uninstall.yml",
        )
        try:
            ansible.verfiy_auth()
        except ValueError as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
        uninstall_command = ansible.get_command()
        result = ansible.run_command(uninstall_command)
        return result

    return app
