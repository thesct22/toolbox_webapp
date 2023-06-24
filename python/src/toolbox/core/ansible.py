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
        super().__init__()
        self.run_folder = data["run_folder"]
        self.playbook = data["playbook"]
        self.inventory = data["inventory"]
        self.tags = data["tags"]
        self.extra_vars = data["extra_vars"]
        self.user = data["user"]
        self.password = data["password"]
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
    user: str = Field(
        ...,
        description="The user to run ansible as.",
    )
    password: str = Field(
        ...,
        description="The password for the user.",
    )
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

    def get_command(self):
        """Get the ansible command."""
        command = [
            "ansible-playbook",
            self.playbook,
            "-i",
            self.inventory,
            "-u",
            self.user,
            "-e",
            f"ansible_ssh_pass={self.password}",
            "-v" * self.verbosity,
        ]
        if self.tags:
            command.append("--tags")
            command.append(",".join(self.tags))
        for key, value in self.extra_vars.items():
            command.append("-e")
            command.append(f"{key}={value}")
        return command

    def get_ping_command(self):
        """Get the ansible ping command."""
        command = [
            "ansible",
            "-i",
            self.inventory,
            "-u",
            self.user,
            "-e",
            f"ansible_ssh_pass={self.password}",
            "-v" * self.verbosity,
            "all",
            "-m",
            "ping",
        ]
        return command

    def run_command(self, command):
        """Run the ansible command."""
        output = subprocess.run(command, cwd=self.run_folder, check=True)
        if output.returncode != 0:
            raise ValueError("Failed to run ansible.")
        return output.stdout.decode("utf-8")
