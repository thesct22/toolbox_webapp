"""Class for handling the list of installable software and their tags."""

import re
from typing import Dict, List, Union

from pydantic import BaseModel, Field, validator
from toolbox.helpers.read_tags import read_tags_helper


class Tags(BaseModel):
    """
    Base class for handling the list of software and their tags.

    Attributes:
        tags (Dict[str, List[str]]): The tags for the installable software.
    """

    tags: List[Dict[str, Union[str, List[str]]]] = Field(
        [],
        description="The tags for the software.",
    )

    def __init__(self):
        """Initialize the tags."""
        super().__init__()
        self.tags = []

    @validator("tags")
    def validate_tags(cls, tags):
        """Validate the tags."""
        for tag in tags:
            if "title" not in tag:
                raise ValueError("Title not found in tag.")
            if "tags" not in tag:
                raise ValueError("Tags not found in tag.")
            if not isinstance(tag["tags"], list):
                raise ValueError("Tags must be a list.")
            if not isinstance(tag["title"], str):
                raise ValueError("Title must be a string.")
            for tag_name in tag["tags"]:
                if not isinstance(tag_name, str):
                    raise ValueError("Tag name must be a string.")
                if re.match(r"^[a-zA-Z0-9_]+$", tag_name) is None:
                    raise ValueError(
                        f"Tag value '{tag_name}' for '{tag['title']}' is invalid."
                        f"Only alphanumeric characters and underscores are allowed."
                    )
                if not tag_name.islower():
                    raise ValueError(
                        f"Tag value '{tag_name}' for '{tag['title']}' is invalid."
                        f"Only lowercase characters are allowed."
                    )
            if re.match(r"^[a-zA-Z0-9_\-\.\/ ]+$", tag["title"]) is None:
                raise ValueError(
                    f"Software naming '{tag['title']}' is invalid."
                    f"Only alphanumeric characters, hyphens, underscores, dots, slashes and spaces are allowed."
                )
        return tags

    def get_tags(self):
        """Return the tags."""
        return self.tags


class InstallationTags(Tags):
    """
    Class for handling the list of installable software and their tags.

    Attributes:
        tags (Dict[str, List[str]]): The tags for the installable software.
    """

    def __init__(self):
        """Initialize the tags."""
        super().__init__()

    def read_tags_from_playbooks(self):
        """Read all the tags inside ansible/roles/xyz/tasks/main.yml and return them as a key-value pair."""
        self.tags = read_tags_helper(install_tags=True)


class UninstallationTags(Tags):
    """
    Class for handling the list of software to uninstall and their tags.

    Attributes:
        tags (Dict[str, List[str]]): The tags for the software to uninstall.
    """

    def __init__(self):
        """Initialize the tags."""
        super().__init__()

    def read_tags_from_playbooks(self):
        """Read all the tags inside ansible/roles/xyz/tasks/main.yml and return them as a key-value pair."""
        self.tags = read_tags_helper(install_tags=False)
