"""This module contains unit tests for the core/file module."""
from pathlib import Path

import pytest
from toolbox.core.file import AnsibleRootFolder, CustomFiles, File, Folder


@pytest.fixture
def root_folder(tmp_path: Path):
    """Returns a temporary folder for testing."""
    folder = tmp_path / "ansible"
    folder.mkdir()
    return folder


def test_folder_create_and_delete(root_folder: Path):
    """Test the folder create and delete methods."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    assert not folder.path.exists()
    folder.create()
    print(folder.path)
    assert folder.path.exists()
    folder.delete()
    # deletes the folder path from the singleton as well
    folder = Folder(root_folder / "roles" / "test")
    assert not folder.path.exists()


def test_file_create_and_delete(root_folder: Path):
    """Test the file create and delete methods."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    file.path.parent.mkdir(parents=True)
    assert not file.path.exists()
    file.create()
    assert file.path.exists()
    file.delete()
    # deletes the file path from the singleton as well
    file = File(root_folder / "roles" / "test" / "test.txt")
    assert not file.path.exists()


def test_folder_rename(root_folder: Path):
    """Test the folder rename method."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    assert not folder.path.exists()
    folder.create()
    assert folder.path.exists()
    folder.rename("test2")
    assert folder.path.exists()
    folder.delete()
    # deletes the folder path from the singleton as well
    folder = Folder(root_folder / "roles" / "test2")
    assert not folder.path.exists()


def test_file_rename(root_folder: Path):
    """Test the file rename method."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    file.path.parent.mkdir(parents=True)
    assert not file.path.exists()
    file.create()
    assert file.path.exists()
    file.rename("test2.txt")
    assert file.path.exists()
    file.delete()
    # deletes the file path from the singleton as well
    file = File(root_folder / "roles" / "test" / "test2.txt")
    assert not file.path.exists()


def test_folder_force_delete(root_folder: Path):
    """Test the folder force delete method."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    assert not folder.path.exists()
    folder.create()
    assert folder.path.exists()
    folder.force_delete()
    # deletes the folder path from the singleton as well
    folder = Folder(root_folder / "roles" / "test")
    assert not folder.path.exists()


def test_folder_non_empty_delete(root_folder: Path):
    """Test the folder delete method when the folder is non-empty."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    assert not folder.path.exists()
    folder.create()
    assert folder.path.exists()
    folder.path.joinpath("test.txt").write_text("test")
    assert folder.path.joinpath("test.txt").exists()
    with pytest.raises(ValueError):
        folder.delete()
    folder.force_delete()
    # deletes the folder path from the singleton as well
    folder = Folder(root_folder / "roles" / "test")
    assert not folder.path.exists()


def test_folder_path_without_ansible(root_folder: Path):
    """Test the folder path without ansible folder."""
    with pytest.raises(ValueError):
        Folder(root_folder.parent / "roles" / "test")


def test_file_path_without_ansible(root_folder: Path):
    """Test the file path without ansible folder."""
    with pytest.raises(ValueError):
        File(root_folder.parent / "roles" / "test" / "test.txt")


def test_folder_path_without_roles(root_folder: Path):
    """Test the folder path without roles folder."""
    with pytest.raises(ValueError):
        Folder(root_folder / "test")


def test_file_path_without_roles(root_folder: Path):
    """Test the file path without roles folder."""
    with pytest.raises(ValueError):
        File(root_folder / "test" / "test.txt")


def test_folder_get_nth_parent(root_folder: Path):
    """Test the folder get_nth_parent method."""
    folder = Folder(root_folder / "roles" / "test")
    assert folder.get_nth_parent(1) == root_folder


def test_file_get_nth_parent(root_folder: Path):
    """Test the file get_nth_parent method."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    assert file.get_nth_parent(2) == root_folder


def test_folder_check_if_folder_exists(root_folder: Path):
    """Test the folder check_if_folder_exists method."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    assert not folder.path.exists()
    folder.create()
    # assert folder.check_if_folder() doesn't raise an error
    assert folder.check_if_folder() is None
    folder.delete()
    with pytest.raises(ValueError):
        folder = Folder(root_folder / "roles" / "test")
        folder.check_if_folder()


def test_file_check_if_file_exists(root_folder: Path):
    """Test the file check_if_file_exists method."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    file.path.parent.mkdir(parents=True)
    assert not file.path.exists()
    file.create()
    # assert file.check_if_file() doesn't raise an error
    assert file.check_if_file() is None
    file.delete()
    with pytest.raises(ValueError):
        file = File(root_folder / "roles" / "test" / "test.txt")
        file.check_if_file()


def test_folder_get_name(root_folder: Path):
    """Test the folder get_name method."""
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    folder.create()
    assert folder.get_name() == "test"


def test_file_get_name(root_folder: Path):
    """Test the file get_name method."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    file.path.parent.mkdir(parents=True)
    file.create()
    assert file.get_name() == "test.txt"


def test_folder_not_exist_validation_error(root_folder: Path):
    """Test the folder not exist validation error."""
    folder = Folder(root_folder / "roles" / "test")
    with pytest.raises(ValueError):
        folder.check_if_folder()


def test_file_not_exist_validation_error(root_folder: Path):
    """Test the file not exist validation error."""
    file = File(root_folder / "roles" / "test" / "test.txt")
    with pytest.raises(ValueError):
        file.check_if_file()


def test_AnsibleRootFolder_get_items(root_folder: Path):
    """Test the AnsibleRootFolder get_items method."""
    ansible_root_folder = AnsibleRootFolder(root_folder)
    expected_result = [
        {"is_file": False, "name": "ansible", "path": Path(root_folder), "items": []}
    ]
    actual_result = ansible_root_folder.get_items()
    assert actual_result == expected_result
    folder = Folder(root_folder / "roles" / "test")
    folder.path.parent.mkdir(parents=True)
    folder.create()
    expected_result = [
        {
            "is_file": False,
            "name": "ansible",
            "path": Path(root_folder),
            "items": [
                {
                    "is_file": False,
                    "name": "roles",
                    "path": Path(root_folder / "roles"),
                    "items": [
                        {
                            "is_file": False,
                            "name": "test",
                            "path": Path(root_folder / "roles" / "test"),
                            "items": [],
                        }
                    ],
                }
            ],
        }
    ]
    actual_result = ansible_root_folder.get_items()
    assert sorted(actual_result, key=lambda x: x['name']) == sorted(expected_result, key=lambda x: x['name'])


def test_CustomFiles_get_inventory(root_folder: Path):
    """Test the CustomFiles get_inventory method."""
    custom_files = CustomFiles(root_folder)
    root_folder.joinpath("inventory").mkdir()
    assert custom_files.get_inventory() == []
    folder = Folder(root_folder / "inventory" / "test")
    folder.create()
    file = File(root_folder / "inventory" / "test.txt")
    file.create()
    expected_result = [
        {
            "is_file": True,
            "name": "test.txt",
            "path": Path(root_folder / "inventory" / "test.txt"),
        },
        {
            "is_file": False,
            "name": "test",
            "path": Path(root_folder / "inventory" / "test"),
            "items": [],
        },
    ]
    actual_result = custom_files.get_inventory()
    assert sorted(actual_result, key=lambda x: x['name']) == sorted(expected_result, key=lambda x: x['name'])


def test_CustomFiles_get_playbooks(root_folder: Path):
    """Test the CustomFiles get_playbooks method."""
    custom_files = CustomFiles(root_folder)
    root_folder.joinpath("roles").mkdir()
    assert custom_files.get_playbooks() == []
    folder = Folder(root_folder / "roles" / "test")
    folder.create()
    file1 = File(root_folder / "test1.yml")
    file1.create()
    file2 = File(root_folder / "test2.yaml")
    file2.create()
    file3 = File(root_folder / "roles" / "test3.yml")
    file3.create()
    expected_result = [
        {"is_file": True, "name": "test1.yml", "path": Path(root_folder / "test1.yml")},
        {
            "is_file": True,
            "name": "test2.yaml",
            "path": Path(root_folder / "test2.yaml"),
        },
    ]
    actual_result = custom_files.get_playbooks()
    assert sorted(actual_result, key=lambda x: x['name']) == sorted(expected_result, key=lambda x: x['name'])
