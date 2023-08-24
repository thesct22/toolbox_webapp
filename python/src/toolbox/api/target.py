"""Target API endpoints."""

from json import JSONDecodeError

from fastapi import FastAPI, HTTPException, Request
from toolbox.core.ansible import Ansible
from toolbox.core.rsakey import RSAKey
from toolbox.helpers.config_target import config_target


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
        try:
            data = await request.json()
        except JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="No data provided or malformed data."
            )
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        try:
            if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
                raise HTTPException(
                    status_code=400, detail="Missing hosts, user or password."
                )
        except KeyError:
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
            print(hosts, user, password)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=str("Missing hosts, user or password, or malformed data."),
            )
        if hosts == "" or user == "" or password == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        hosts = hosts.split(",")
        try:
            current_host = hosts[0]
            for host in hosts:
                current_host = host
                config_target(host, user, password)
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=f'Error: "{str(e)}" on {current_host}.'
            )
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
        try:
            data = await request.json()
        except JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="No data provided or malformed data."
            )
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data == {}:
            raise HTTPException(status_code=400, detail="No data provided.")
        try:
            if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
                raise HTTPException(
                    status_code=400, detail="Missing hosts, user or password."
                )
        except KeyError:
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=str("Missing hosts, user or password, or malformed data."),
            )
        if hosts == "" or user == "" or password == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        ansible = Ansible(
            inventory=hosts,
            user=user,
            password=password,
            playbook="ping.yml",
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
        try:
            data = await request.json()
        except JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="No data provided or malformed data."
            )
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data == {}:
            raise HTTPException(status_code=400, detail="No data provided.")
        try:
            if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
                raise HTTPException(
                    status_code=400, detail="Missing hosts, user or password."
                )
        except KeyError:
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        try:
            if data["tags"] == []:
                raise HTTPException(status_code=400, detail="No tags provided.")
        except KeyError:
            raise HTTPException(status_code=400, detail="No tags provided.")
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=str("Missing hosts, user or password, or malformed data."),
            )
        if hosts == "" or user == "" or password == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
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
            raise HTTPException(status_code=400, detail=str(e))
        install_command = ansible.get_command()
        try:
            result = ansible.run_command(install_command)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
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
        try:
            data = await request.json()
        except JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="No data provided or malformed data."
            )
        if data is None:
            raise HTTPException(status_code=400, detail="No data provided.")
        if data == {}:
            raise HTTPException(status_code=400, detail="No data provided.")
        try:
            if data["hosts"] == "" or data["user"] == "" or data["password"] == "":
                raise HTTPException(
                    status_code=400, detail="Missing hosts, user or password."
                )
        except KeyError:
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
        try:
            if data["tags"] == []:
                raise HTTPException(status_code=400, detail="No tags provided.")
        except KeyError:
            raise HTTPException(status_code=400, detail="No tags provided.")
        try:
            hosts = RSAKey().decrypt(data["hosts"])
            user = RSAKey().decrypt(data["user"])
            password = RSAKey().decrypt(data["password"])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=str("Missing hosts, user or password, or malformed data."),
            )
        if hosts == "" or user == "" or password == "":
            raise HTTPException(
                status_code=400, detail="Missing hosts, user or password."
            )
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
            raise HTTPException(status_code=400, detail=str(e))
        uninstall_command = ansible.get_command()
        try:
            result = ansible.run_command(uninstall_command)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return result

    return app
