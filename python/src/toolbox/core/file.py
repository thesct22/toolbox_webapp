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
    def path_is_file(cls, v: Path):
        """Validate if path is a file."""
        if not v.is_file():
            raise ValueError(f"Path {v} is not a file")
        return v

    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    @validator("path")
    def file_is_in_ansible_or_inventory(cls, v: Path):
        """Validate if path is in the ansible folder or ansible/inventory folder."""
        if not v.parent.name == "ansible" and (
            not v.parent.name == "inventory" or not v.parent.parent.name == "ansible"
        ):
            raise ValueError(
                f"{v} is not from the ansible main folder or inventory folder"
            )
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize a File object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def read_content(self) -> str:
        """Return the content of the file."""
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str) -> bool:
        """Write content to the file."""
        try:
            with open(self.path, "w") as f:
                f.write(content)
            return True
        except Exception:
            return False

    def rename(self, new_name: str) -> Path:
        """Rename the file."""
        new_path = self.path.parent / new_name
        self.path.rename(new_path)
        self.path = new_path
        return self.path

    def get_name(self) -> str:
        """Return the name of the file."""
        return self.path.name

    def delete(self) -> None:
        """Delete the file."""
        self.path.unlink()
        self.path = Path("")


class Folder(FileBase):
    """Class for handling folders."""

    @validator("path")
    def path_is_folder(cls, v: Path):
        """Validate if path is a folder."""
        if not v.is_dir():
            raise ValueError(f"Path {v} is not a folder")
        return v

    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize a Folder object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def get_name(self) -> str:
        """Return the name of the folder."""
        return self.path.name

    def get_items(self) -> List[Dict[str, Union[bool, Path]]]:
        """Return a list of dictionaries with the items in the folder."""
        return list(
            map(lambda x: {"is_file": x.is_file(), "path": x}, self.path.iterdir())
        )


class FileCreate(FileBase):
    """
    Class for handling file creation.

        > Had to create a new class because of the validators in File and Folder classes
        > These validators are not needed when creating files and folders because they don't exist yet.
    """

    @validator("path")
    def path_is_file(cls, v: Path):
        """Validate if path is a file."""
        if v.is_file():
            raise ValueError(f"Path {v} is already a file")
        return v

    #  validate if file has ansible in its path
    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    #  validate if file's immediate parent is ansible or ansible/inventory
    @validator("path")
    def file_is_in_ansible_or_inventory(cls, v: Path):
        """Validate if path is in the ansible folder or ansible/inventory folder."""
        if not v.parent.name == "ansible" and (
            not v.parent.name == "inventory" or not v.parent.parent.name == "ansible"
        ):
            raise ValueError(
                f"{v} is not from the ansible main folder or inventory folder"
            )
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize a FileCreate object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def create(self) -> None:
        """Create the file."""
        self.path.touch()


class FolderCreate(FileBase):
    """
    Class for handling folder creation.

        > Had to create a new class because of the validators in File and Folder classes
        > These validators are not needed when creating files and folders because they don't exist yet.
    """

    @validator("path")
    def path_is_folder(cls, v: Path):
        """Validate if path is a folder."""
        if v.is_dir():
            raise ValueError(f"Path {v} is already a folder")
        return v

    @validator("path")
    def path_has_ansible(cls, v: Path):
        """Validate if path is in the ansible folder."""
        if "ansible" not in v.parts:
            raise ValueError(f"{v} is not from the ansible folder")
        return v

    @validator("path")
    def folder_is_in_ansible_or_inventory(cls, v: Path):
        """Validate if path is in the ansible folder or ansible/inventory folder."""
        if not v.parent.name == "ansible" and (
            not v.parent.name == "inventory" or not v.parent.parent.name == "ansible"
        ):
            raise ValueError(
                f"{v} is not from the ansible main folder or inventory folder"
            )
        return v

    def __init__(self, path: Union[str, Path]):
        """Initialize a FolderCreate object."""
        super().__init__(path=path)
        self.path = self.path.resolve()

    def create(self) -> None:
        """Create the folder."""
        self.path.mkdir(parents=True, exist_ok=True)


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
                items.append({"is_file": True, "path": item})
            elif item.name == "inventory":
                items.append(
                    {
                        "is_file": False,
                        "path": item,
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
                items.append({"is_file": True, "path": item})
            else:
                items.append(
                    {
                        "is_file": False,
                        "path": item,
                        "items": self.__get_items_recursive(item),
                    }
                )
        return items
