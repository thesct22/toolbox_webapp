"""File and Folder classes for handling files and folders."""

from pathlib import Path
from typing import Dict, List, Union

from pydantic import BaseModel, Field, validator


class FileBase(BaseModel):
    """Base class for File and Folder."""

    path: Path = Field(..., description="Path to file")

    @validator("path", pre=True)
    def path_to_pathlib(cls, v: Union[str, Path]):
        """Convert path to pathlib.Path object."""
        if isinstance(v, str):
            return Path(v)
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize a FileBase object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def __str__(self):
        """Return the path as a string when the object is casted to a string."""
        return str(self.path)

    # same as __str__ but machine readable
    def __repr__(self):
        """Return the path as a string when the object is casted to a string."""
        return f"{self.__class__.__name__}(path={self.path})"

    def __eq__(self, other):
        """Return True if the path is the same as the other path."""
        if isinstance(other, self.__class__):
            return self.path == other.path
        return False

    def get_nth_parent(self, n: int) -> Path:
        """Return the nth parent of the path."""
        return self.path.parents[n]


class File(FileBase):
    """Class for handling files."""

    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    @validator("path")
    def file_is_in_ansible_inventory_or_roles(cls, v: Path):
        """Validate if path is in the ansible root, ansible/inventory or ansible/roles folders."""
        index = -1
        for i, part in enumerate(v.parts):
            if part == "ansible":
                index = i
        if index == -1:
            raise ValueError(f"{v} is not in the ansible folder")
        if v.parts[index + 1] == "inventory" or v.parts[index + 1] == "roles":
            return v
        if v.parent == "ansible":
            return v
        raise ValueError(
            f"{v} is not from the ansible root, ansible/inventory or ansible/roles folders"
        )

    def __init__(self, path: Union[str, Path]):
        """Initialize a File object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def check_if_file(self) -> None:
        """Check if the path is a file."""
        if not self.path.is_file():
            raise ValueError(f"{self.path} is not a file.")

    def check_if_not_in_custom_roles_folder(self) -> None:
        """Check if the path is in the roles folder but not in the custom roles folder."""
        index = -1
        for i, part in enumerate(self.path.parts):
            if part == "ansible":
                index = i
        if index == -1:
            raise ValueError(f"{self.path} is not in the ansible folder")
        if self.path.parts[index + 1] == "roles":
            if self.path.parts[index + 2] != "custom":
                raise ValueError(
                    f"{self.path} is in the roles folder but not in the custom roles folder"
                )

    def read_content(self) -> str:
        """Return the content of the file."""
        self.check_if_file()
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str) -> bool:
        """Write content to the file."""
        self.check_if_file()
        self.check_if_not_in_custom_roles_folder()
        try:
            with open(self.path, "w") as f:
                f.write(content)
            return True
        except Exception:
            return False

    def create(self) -> None:
        """Create the file."""
        if self.path.is_file():
            raise ValueError(f"{self.path} already exists.")
        self.check_if_not_in_custom_roles_folder()
        self.path.touch()

    def rename(self, new_name: str) -> Path:
        """Rename the file."""
        self.check_if_file()
        self.check_if_not_in_custom_roles_folder()
        new_path = self.path.parent / new_name
        self.path.rename(new_path)
        self.path = new_path
        return self.path

    def delete(self) -> None:
        """Delete the file."""
        self.check_if_file()
        self.check_if_not_in_custom_roles_folder()
        self.path.unlink()
        self.path = Path("")

    def get_name(self) -> str:
        """Return the name of the file."""
        self.check_if_file()
        return self.path.name


class Folder(FileBase):
    """Class for handling folders."""

    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    @validator("path")
    def folder_is_in_ansible_inventory_or_roles(cls, v: Path):
        """Validate if path is in the ansible root, ansible/inventory or ansible/roles folders."""
        index = -1
        for i, part in enumerate(v.parts):
            if part == "ansible":
                index = i
        if index == -1:
            raise ValueError(f"{v} is not in the ansible folder")
        if v.parts[index + 1] == "inventory" or v.parts[index + 1] == "roles":
            return v
        raise ValueError(
            f"{v} is not ansible/inventory or ansible/roles folders or their subfolders"
        )

    def __init__(self, path: Union[str, Path]):
        """Initialize a Folder object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def check_if_folder(self) -> None:
        """Check if the path is a folder."""
        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a folder.")

    def check_if_not_in_custom_roles_folder(self) -> None:
        """Check if the path is in the roles folder but not in the custom roles folder."""
        index = -1
        for i, part in enumerate(self.path.parts):
            if part == "ansible":
                index = i
        if index == -1:
            raise ValueError(f"{self.path} is not in the ansible folder")
        if self.path.parts[index + 1] == "roles":
            if self.path.parts[index + 2] != "custom":
                raise ValueError(
                    f"{self.path} is in the roles folder but not in the custom roles folder"
                )

    def get_items(self) -> List[Dict[str, Union[bool, Path]]]:
        """Return a list of dictionaries with the items in the folder."""
        self.check_if_folder()
        return list(
            map(lambda x: {"is_file": x.is_file(), "path": x}, self.path.iterdir())
        )

    def create(self) -> None:
        """Create the folder."""
        if self.path.is_dir():
            raise ValueError(f"{self.path} already exists.")
        self.check_if_not_in_custom_roles_folder()
        self.path.mkdir()

    def rename(self, new_name: str) -> Path:
        """Rename the folder."""
        self.check_if_folder()
        self.check_if_not_in_custom_roles_folder()
        new_path = self.path.parent / new_name
        self.path.rename(new_path)
        self.path = new_path
        return self.path

    def delete(self) -> None:
        """Delete the folder."""
        self.check_if_folder()
        self.check_if_not_in_custom_roles_folder()
        # check if folder is empty
        if len(self.get_items()) > 0:
            raise ValueError(f"{self.path} is not empty.")
        self.path.rmdir()
        self.path = Path("")

    def force_delete(self) -> None:
        """Force delete the folder."""
        self.check_if_folder()
        self.check_if_not_in_custom_roles_folder()
        # delete all files and folders in the folder
        for item in self.get_items():
            if item["is_file"]:
                if not isinstance(item["path"], bool):
                    File(item["path"]).delete()
            else:
                if not isinstance(item["path"], bool):
                    Folder(item["path"]).force_delete()
        self.path.rmdir()
        self.path = Path("")

    def get_name(self) -> str:
        """Return the name of the folder."""
        return self.path.name


class AnsibleRootFolder(FileBase):
    """Class for handling the ansible root folder."""

    @validator("path")
    def path_is_ansible_root(cls, v: Path):
        """Validate if path is the ansible root folder."""
        if not v.name == "ansible":
            raise ValueError(f"{v} is not the ansible root folder")
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize an AnsibleRootFolder object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def get_items(self) -> List[Dict[str, Union[bool, str, list]]]:
        """
        Return all the items in the ansible root folder.

        Only return the all the files in the ansible root folder and
        iteratively everything inside the inventory folder.
        Other folders and files inside them are ignored for security reasons.

        Returns:
            List[Dict[str, Union[bool, str, list]]]: List of dictionaries with the items in the ansible root folder.
        """
        items = []
        for item in self.path.iterdir():
            if item.is_file():
                items.append({"is_file": True, "path": item, "name": item.name})
            elif item.name == "inventory" or item.name == "roles":
                items.append(
                    {
                        "is_file": False,
                        "path": item,
                        "name": item.name,
                        "items": self.__get_items_recursive(item),
                    }
                )
            else:
                continue
        return items

    def __get_items_recursive(
        self, path: Path
    ) -> List[Dict[str, Union[bool, str, list]]]:
        """
        Recursive function to get all the items in a folder.

        Args:
            path (Path): The path to the folder.
        Returns:
            List[Dict[str, Union[bool, str, list]]]: List of dictionaries with the items in the folder.
        """
        items = []
        for item in path.iterdir():
            if item.is_file():
                items.append({"is_file": True, "path": item, "name": item.name})
            else:
                items.append(
                    {
                        "is_file": False,
                        "path": item,
                        "name": item.name,
                        "items": self.__get_items_recursive(item),
                    }
                )
        return items
