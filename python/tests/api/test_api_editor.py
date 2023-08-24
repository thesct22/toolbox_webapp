from pathlib import Path

from fastapi.testclient import TestClient
import pytest
from toolbox.main import app

client = TestClient(app)


@pytest.fixture
def tmp_ansible(tmp_path: Path):
    """Create a temporary ansible folder for testing."""
    ansible = tmp_path / "ansible"
    ansible.mkdir()
    yield ansible


# /api/editor/files
def test_editor_get_files():
    """Test the /api/editor/files endpoint to get all files."""
    response = client.get("/api/editor/files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# /api/editor/file?path={}
def test_editor_get_file_with_file(tmp_ansible: Path):
    """Test the /api/editor/file/read endpoint to get a file."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.get(f"/api/editor/file/read?path={p}")
    assert response.status_code == 200
    assert response.json() == {"content": "test"}


def test_editor_get_file_with_file_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/file/read endpoint to get a file that is not in the ansible folder."""
    p = tmp_ansible.parent / "test.txt"
    p.write_text("test")
    response = client.get(f"/api/editor/file/read?path={p}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for File\npath\n  This file is not from the ansible folder (type=value_error)"
    }


def test_editor_get_file_with_no_file(tmp_ansible: Path):
    """Test the /api/editor/file/read endpoint without a path parameter."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.get("/api/editor/file/read")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "path"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_editor_get_file_with_non_existing_file(tmp_ansible: Path):
    """Test the /api/editor/file/read endpoint with a non existing file."""
    response = client.get(f"/api/editor/file/read?path={tmp_ansible / 'test.txt'}")
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a file."}


# /api/editor/file/write
def test_editor_write_file(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint to write a file."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/write",
        json={"content": "test_writing", "path": p.as_posix()},
    )
    assert response.status_code == 200
    assert response.json() == {"written": "test_writing", "success": "true"}
    read_response = client.get(f"/api/editor/file/read?path={p}")
    assert read_response.status_code == 200
    assert read_response.json() == {"content": "test_writing"}


def test_editor_write_file_with_non_existing_file(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint to write a file that does not exist."""
    response = client.post(
        "/api/editor/file/write",
        json={"content": "test_writing", "path": (tmp_ansible / "test.txt").as_posix()},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a file."}


def test_editor_write_file_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint to write a file that is not in the ansible folder."""
    p = tmp_ansible.parent / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/write",
        json={"content": "test_writing", "path": p.as_posix()},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for File\npath\n  This file is not from the ansible folder (type=value_error)"
    }


def test_editor_write_file_with_no_content(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint without passing content parameter."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/write", json={"path": p.as_posix()})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or content."}


def test_editor_write_file_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint without passing path parameter."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/write", json={"content": "test_writing"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or content."}


def test_editor_write_file_with_no_path_and_no_content(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint with empty json."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/write", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_write_file_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint with no json."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/write")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_write_file_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint with empty path parameter."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/write", json={"content": "test_writing", "path": ""}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or content."}


def test_editor_write_file_with_empty_content(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint with empty content parameter."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/write", json={"content": "", "path": p.as_posix()}
    )
    assert response.status_code == 200
    assert response.json() == {"written": "", "success": "true"}
    assert p.read_text() == ""
    read_response = client.get(f"/api/editor/file/read?path={p}")
    assert read_response.status_code == 200
    assert read_response.json() == {"content": ""}


def test_editor_write_file_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/file/write endpoint with wrong data."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/write", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or content."}


# /api/editor/file/create
def test_editor_create_file(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file."""
    response = client.post(
        "/api/editor/file/create", json={"path": (tmp_ansible / "test.txt").as_posix()}
    )
    assert response.status_code == 200
    assert response.json() == {"created": "true"}
    assert (tmp_ansible / "test.txt").exists()


def test_editor_create_file_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file that is not in the ansible folder."""
    response = client.post(
        "/api/editor/file/create",
        json={"path": (tmp_ansible.parent / "test.txt").as_posix()},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This file is not from the ansible folder"}


def test_editor_create_file_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file without passing path parameter."""
    response = client.post("/api/editor/file/create", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_create_file_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file with empty json."""
    response = client.post("/api/editor/file/create")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_create_file_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file with empty path parameter."""
    response = client.post("/api/editor/file/create", json={"path": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_create_file_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file with wrong data."""
    response = client.post("/api/editor/file/create", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_create_file_with_existing_file(tmp_ansible: Path):
    """Test the /api/editor/file/create endpoint to create a file with an existing file."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/create", json={"path": p.as_posix()})
    assert response.status_code == 404
    assert response.json() == {"detail": "This file already exists."}


# /api/editor/file/delete
def test_editor_delete_file(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/delete", json={"path": p.as_posix()})
    assert response.status_code == 200
    assert response.json() == {"deleted": "true"}
    assert not p.exists()


def test_editor_delete_file_that_does_not_exist(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file that does not exist."""
    response = client.post(
        "/api/editor/file/delete", json={"path": (tmp_ansible / "test.txt").as_posix()}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a file."}


def test_editor_delete_file_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file that is not in the ansible folder."""
    p = tmp_ansible.parent / "test.txt"
    p.write_text("test")
    response = client.post("/api/editor/file/delete", json={"path": p.as_posix()})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for File\npath\n  This file is not from the ansible folder (type=value_error)"
    }


def test_editor_delete_file_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file without passing path parameter."""
    response = client.post("/api/editor/file/delete", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_file_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file with empty json."""
    response = client.post("/api/editor/file/delete")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_file_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file with empty path parameter."""
    response = client.post("/api/editor/file/delete", json={"path": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_delete_file_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/file/delete endpoint to delete a file with wrong data."""
    response = client.post("/api/editor/file/delete", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


# /api/editor/file/rename
def test_editor_rename_file(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint."""
    p = tmp_ansible / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/rename",
        json={"path": p.as_posix(), "new_path": (tmp_ansible / "test2.txt").as_posix()},
    )
    assert response.status_code == 200
    assert response.json() == {"new_path": (tmp_ansible / "test2.txt").as_posix()}
    assert (tmp_ansible / "test2.txt").exists()
    assert not p.exists()


def test_editor_rename_file_that_does_not_exist(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file that does not exist."""
    response = client.post(
        "/api/editor/file/rename",
        json={
            "path": (tmp_ansible / "test.txt").as_posix(),
            "new_path": (tmp_ansible / "test2.txt").as_posix(),
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a file."}


def test_editor_rename_file_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file that is not in the ansible folder."""
    p = tmp_ansible.parent / "test.txt"
    p.write_text("test")
    response = client.post(
        "/api/editor/file/rename",
        json={"path": p.as_posix(), "new_path": (tmp_ansible / "test2.txt").as_posix()},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for File\npath\n  This file is not from the ansible folder (type=value_error)"
    }


def test_editor_rename_file_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file without passing path parameter."""
    response = client.post(
        "/api/editor/file/rename",
        json={"new_path": (tmp_ansible / "test2.txt").as_posix()},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_file_with_no_new_path(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file without passing new_path parameter."""
    response = client.post(
        "/api/editor/file/rename", json={"path": (tmp_ansible / "test.txt").as_posix()}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_file_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file with empty json."""
    response = client.post("/api/editor/file/rename")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_rename_file_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file with empty path parameter."""
    response = client.post(
        "/api/editor/file/rename",
        json={"path": "", "new_path": (tmp_ansible / "test2.txt").as_posix()},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_file_with_empty_new_path(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file with empty new_path parameter."""
    response = client.post(
        "/api/editor/file/rename",
        json={"path": (tmp_ansible / "test.txt").as_posix(), "new_path": ""},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_file_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/file/rename endpoint to rename a file with wrong data."""
    response = client.post("/api/editor/file/rename", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


# /api/editor/folder/create
def test_editor_create_folder_inside_inventory(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder."""
    (tmp_ansible / "inventory").mkdir()
    response = client.post(
        "/api/editor/folder/create",
        json={"path": (tmp_ansible / "inventory" / "test").as_posix()},
    )
    assert response.status_code == 200
    assert response.json() == {"created": "true"}
    assert (tmp_ansible / "inventory" / "test").exists()


def test_editor_create_folder_inside_roles(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder."""
    (tmp_ansible / "roles").mkdir()
    response = client.post(
        "/api/editor/folder/create",
        json={"path": (tmp_ansible / "roles" / "test").as_posix()},
    )
    assert response.status_code == 200
    assert response.json() == {"created": "true"}
    assert (tmp_ansible / "roles" / "test").exists()


def test_editor_create_folder_outside_inventory_and_roles(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder."""
    response = client.post(
        "/api/editor/folder/create", json={"path": (tmp_ansible / "test").as_posix()}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "This folder is not ansible/inventory or ansible/roles folders or their subfolders"
    }
    assert not (tmp_ansible / "test").exists()


def test_editor_create_folder_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder that is not in the ansible folder."""
    response = client.post(
        "/api/editor/folder/create",
        json={"path": (tmp_ansible.parent / "test").as_posix()},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This folder is not from the ansible folder"}


def test_editor_create_folder_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder without passing path parameter."""
    response = client.post("/api/editor/folder/create", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_create_folder_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder with empty json."""
    response = client.post("/api/editor/folder/create")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_create_folder_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder with empty path parameter."""
    response = client.post("/api/editor/folder/create", json={"path": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_create_folder_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder with wrong data."""
    response = client.post("/api/editor/folder/create", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_create_folder_with_existing_folder(tmp_ansible: Path):
    """Test the /api/editor/folder/create endpoint to create a folder with an existing folder."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    p.mkdir()
    response = client.post("/api/editor/folder/create", json={"path": p.as_posix()})
    assert response.status_code == 404
    assert response.json() == {"detail": "This folder already exists."}


# /api/editor/folder/delete
def test_editor_delete_folder(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    p.mkdir()
    response = client.post("/api/editor/folder/delete", json={"path": p.as_posix()})
    assert response.status_code == 200
    assert response.json() == {"deleted": "true"}
    assert not p.exists()


def test_editor_delete_folder_with_files(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder with files in it."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    p.mkdir()
    (p / "test.txt").write_text("test")
    response = client.post("/api/editor/folder/delete", json={"path": p.as_posix()})
    assert response.status_code == 200
    assert response.json() == {"deleted": "get_confirmation"}
    assert p.exists()


def test_editor_delete_folder_that_does_not_exist(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder that does not exist."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    response = client.post("/api/editor/folder/delete", json={"path": p.as_posix()})
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a folder."}


def test_editor_delete_folder_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder that is not in the ansible folder."""
    p = tmp_ansible.parent / "test"
    p.mkdir()
    response = client.post("/api/editor/folder/delete", json={"path": p.as_posix()})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for Folder\npath\n  This folder is not from the ansible folder (type=value_error)"
    }


def test_editor_delete_folder_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder without passing path parameter."""
    response = client.post("/api/editor/folder/delete", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_folder_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder with empty json."""
    response = client.post("/api/editor/folder/delete")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_folder_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder with empty path parameter."""
    response = client.post("/api/editor/folder/delete", json={"path": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_delete_folder_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/folder/delete endpoint to delete a folder with wrong data."""
    response = client.post("/api/editor/folder/delete", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


#  /api/editor/folder/delete/confirmed
def test_editor_delete_folder_confirmed(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    p.mkdir()
    (p / "test.txt").write_text("test")
    response = client.post(
        "/api/editor/folder/delete/confirmed", json={"path": p.as_posix()}
    )
    assert response.status_code == 200
    assert response.json() == {"deleted": "true"}
    assert not p.exists()


def test_editor_delete_folder_confirmed_that_does_not_exist(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder that does not exist."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    response = client.post(
        "/api/editor/folder/delete/confirmed", json={"path": p.as_posix()}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a folder."}


def test_editor_delete_folder_confirmed_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder that is not in the ansible folder."""
    p = tmp_ansible.parent / "test"
    p.mkdir()
    response = client.post(
        "/api/editor/folder/delete/confirmed", json={"path": p.as_posix()}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for Folder\npath\n  This folder is not from the ansible folder (type=value_error)"
    }


def test_editor_delete_folder_confirmed_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder without passing path parameter."""
    response = client.post("/api/editor/folder/delete/confirmed", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_folder_confirmed_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder with empty json."""
    response = client.post("/api/editor/folder/delete/confirmed")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_delete_folder_confirmed_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder with empty path parameter."""
    response = client.post("/api/editor/folder/delete/confirmed", json={"path": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


def test_editor_delete_folder_confirmed_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/folder/delete/confirmed endpoint to delete a folder with wrong data."""
    response = client.post(
        "/api/editor/folder/delete/confirmed", json={"random_header": "test"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path."}


# /api/editor/folder/rename
def test_editor_rename_folder(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint."""
    p = tmp_ansible / "inventory" / "test"
    p.parent.mkdir()
    p.mkdir()
    response = client.post(
        "/api/editor/folder/rename",
        json={
            "path": p.as_posix(),
            "new_path": (tmp_ansible / "inventory" / "test2").as_posix(),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "new_path": (tmp_ansible / "inventory" / "test2").as_posix()
    }
    assert (tmp_ansible / "inventory" / "test2").exists()
    assert not p.exists()


def test_editor_rename_folder_that_does_not_exist(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder that does not exist."""
    response = client.post(
        "/api/editor/folder/rename",
        json={
            "path": (tmp_ansible / "inventory" / "test").as_posix(),
            "new_path": (tmp_ansible / "inventory" / "test2").as_posix(),
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This is not a folder."}


def test_editor_rename_folder_not_in_ansible(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder that is not in the ansible folder."""
    p = tmp_ansible.parent / "test"
    p.mkdir()
    response = client.post(
        "/api/editor/folder/rename",
        json={
            "path": p.as_posix(),
            "new_path": (tmp_ansible / "inventory" / "test2").as_posix(),
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "1 validation error for Folder\npath\n  This folder is not from the ansible folder (type=value_error)"
    }


def test_editor_rename_folder_with_no_path(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder without passing path parameter."""
    response = client.post(
        "/api/editor/folder/rename",
        json={"new_path": (tmp_ansible / "inventory" / "test2").as_posix()},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_folder_with_no_new_path(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder without passing new_path parameter."""
    response = client.post(
        "/api/editor/folder/rename",
        json={"path": (tmp_ansible / "inventory" / "test").as_posix()},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_folder_with_no_data(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder with empty json."""
    response = client.post("/api/editor/folder/rename")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_editor_rename_folder_with_empty_path(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder with empty path parameter."""
    response = client.post(
        "/api/editor/folder/rename",
        json={"path": "", "new_path": (tmp_ansible / "inventory" / "test2").as_posix()},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_folder_with_empty_new_path(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder with empty new_path parameter."""
    response = client.post(
        "/api/editor/folder/rename",
        json={"path": (tmp_ansible / "inventory" / "test").as_posix(), "new_path": ""},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}


def test_editor_rename_folder_with_wrong_data(tmp_ansible: Path):
    """Test the /api/editor/folder/rename endpoint to rename a folder with wrong data."""
    response = client.post("/api/editor/folder/rename", json={"random_header": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing path or new_path."}
