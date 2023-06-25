"""Ansible class for handling the ansible cli commands."""
from pathlib import Path
import subprocess
from typing import Dict, List

from pydantic import BaseModel, Field, validator


class Ansible(BaseModel):
    """
    Base class for handling the ansible cli commands.

    Attributes:
        run_folder (Path): The folder to run ansible from.
        playbook (str): The ansible playbook file.
        inventory (str): The ansible inventory file/hosts.
        tags (List[str]): The ansible tags to run.
        extra_vars (Dict[str, str]): The extra variables to pass to ansible.
        user (str): The user to run ansible as.
        password (str): The password for the user.
        verbosity (int): The verbosity level for ansible.
    """

    def __init__(self, **data):
        """Initialize the ansible class."""
        super().__init__(**data)
        if "run_folder" in data:
            self.run_folder = data["run_folder"]
        if "playbook" in data:
            self.playbook = data["playbook"]
        if "inventory" not in data:
            raise ValueError("Inventory cannot be empty.")
        self.inventory = data["inventory"]
        if "tags" in data:
            self.tags = data["tags"]
        if "extra_vars" in data:
            self.extra_vars = data["extra_vars"]
        if "user" not in data:
            raise ValueError("User cannot be empty.")
        self.user = data["user"]
        if "password" not in data:
            raise ValueError("Password cannot be empty.")
        self.password = data["password"]
        if "verbosity" in data:
            self.verbosity = data["verbosity"]

    run_folder: Path = Field(
        Path(__file__).parent.parent / "ansible",
        description="The folder to run ansible from.",
    )

    playbook: str = Field(
        "install.yml",
        description="The ansible playbook file.",
    )
    inventory: str = Field(
        "roles/hosts",
        description="The ansible inventory file/hosts.",
    )
    tags: List[str] = Field(
        [],
        description="The ansible tags to run.",
    )
    extra_vars: Dict[str, str] = Field(
        {},
        description="The extra variables to pass to ansible.",
    )
    user: str = Field(..., description="The user to run ansible as.", required=True)
    password: str = Field(..., description="The password for the user.", required=True)
    verbosity: int = Field(
        0,
        description="The verbosity level for ansible.",
    )

    @validator("playbook")
    def validate_playbook(cls, playbook):
        """Validate the playbook."""
        if playbook == "":
            raise ValueError("Playbook cannot be empty.")
        return playbook

    @validator("inventory")
    def validate_inventory(cls, inventory):
        """Validate the inventory."""
        if inventory == "":
            raise ValueError("Inventory cannot be empty.")
        return inventory

    @validator("user")
    def validate_user(cls, user):
        """Validate the user."""
        if user == "":
            raise ValueError("User cannot be empty.")
        if user == "root":
            raise ValueError("User cannot be root.")
        return user

    @validator("password")
    def validate_password(cls, password):
        """Validate the password."""
        if password == "":
            raise ValueError("Password cannot be empty.")
        return password

    @validator("verbosity")
    def validate_verbosity(cls, verbosity):
        """Validate the verbosity."""
        if verbosity < 0 or verbosity > 4:
            raise ValueError("Verbosity must be between 0 and 4.")
        return verbosity

    def verfiy_auth(self) -> bool:
        """Verify the username, password and inventory are correct."""
        inventory = self.inventory.split(",")
        for host in inventory:
            command = [
                "sshpass",
                "-p",
                self.password,
                "ssh",
                "-o",
                "PreferredAuthentications=password",
                f"{self.user}@{host}",
                "echo",
                "success",
            ]
            try:
                output = subprocess.run(
                    command,
                    cwd=self.run_folder,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if output.returncode != 0:
                    raise ValueError(
                        "Failed to verify ansible credentials for host: " + host
                    )
                if output.stdout:
                    if output.stdout.decode("utf-8") != "success\n":
                        raise ValueError(
                            "Failed to verify ansible credentials for host: " + host
                        )
            except subprocess.CalledProcessError as e:
                raise ValueError(
                    "Failed to verify ansible credentials for host: " + host
                ) from e
        return True

    def get_command(self):
        """Get the ansible command."""
        if not Path(self.inventory).is_file():
            if self.inventory[-1] != ",":
                self.inventory += ","
        command = [
            "ansible-playbook",
            self.playbook,
            "-i",
            self.inventory,
            "-u",
            self.user,
            "-e",
            f"ansible_become_pass={self.password}",
            "-e",
            "ansible_ssh_pass={self.password}",
        ]
        if self.verbosity > 0:
            command.append("-v" * self.verbosity)
        if self.tags:
            command.append("--tags")
            command.append(",".join(self.tags))
        for key, value in self.extra_vars.items():
            command.append("-e")
            command.append(f"{key}={value}")
        return command

    def get_ping_command(self):
        """Get the ansible ping command."""
        if not Path(self.inventory).is_file():
            if self.inventory[-1] != ",":
                self.inventory += ","
        command = [
            "ansible",
            "all",
            "-i",
            self.inventory,
            "-u",
            self.user,
            "-e",
            f"ansible_ssh_pass={self.password}",
            "-m",
            "ping",
        ]
        if self.verbosity > 0:
            command.append("-v" * self.verbosity)

        return command

    def run_command(self, command):
        """Run the ansible command."""
        try:
            output = subprocess.run(
                command,
                cwd=self.run_folder,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if output.returncode != 0:
                raise ValueError("Failed to run ansible.")
            if output.stdout:
                return output.stdout.decode("utf-8")
        except subprocess.CalledProcessError as e:
            raise ValueError("Failed to run ansible.") from e
        return "Ran ansible successfully."
