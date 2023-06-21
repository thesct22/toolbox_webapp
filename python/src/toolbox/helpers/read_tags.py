"""Helper function to read all the tags inside ansible/roles/xyz/tasks/main.yml and return them as a key-value pair."""

from pathlib import Path
from typing import Dict, List

import yaml


def read_tags_helper(install_tags: bool) -> Dict[str, List[str]]:
    """
    Read all the tags inside ansible/roles/xyz/tasks/main.yml and return them as a key-value pair.

    Args:
        install_tags (bool): Whether to get install tags or uninstall tags.
    Returns:
        Dict[str, List[str]]: The tags as "software name": ["tag1", "tag2"] key-value pairs.
    """
    ansible_roles_dir = Path(__file__).parent.parent / "ansible" / "roles"
    tags = {}
    if not ansible_roles_dir.exists():
        raise ValueError(
            f"Ansible roles directory '{ansible_roles_dir}' does not exist."
        )
    if install_tags:
        for role_dir in ansible_roles_dir.iterdir():
            if not role_dir.is_dir():
                continue
            if not (role_dir / "tasks" / "main.yml").exists():
                continue
            with open(role_dir / "tasks" / "main.yml", "r") as f:
                main_yml = yaml.safe_load(f)
                for task in main_yml:
                    if "name" not in task:
                        continue
                    if "Install" not in task["name"]:
                        continue
                    if "tags" not in task:
                        continue
                    if not isinstance(task["tags"], list):
                        continue
                    tags[str(task["name"]).split("Install")[1].strip()] = task["tags"]
    else:
        for role_dir in ansible_roles_dir.iterdir():
            if not role_dir.is_dir():
                continue
            if not (role_dir / "tasks" / "main.yml").exists():
                continue
            with open(role_dir / "tasks" / "main.yml", "r") as f:
                main_yml = yaml.safe_load(f)
                for task in main_yml:
                    if "name" not in task:
                        continue
                    if "Uninstall" not in task["name"]:
                        continue
                    if "tags" not in task:
                        continue
                    if not isinstance(task["tags"], list):
                        continue
                    tags[str(task["name"]).split("Uninstall")[1].strip()] = task["tags"]
    return tags
