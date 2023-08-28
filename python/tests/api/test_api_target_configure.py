from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest
from toolbox.core.rsakey import encrypt
from toolbox.main import app

client = TestClient(app)


@pytest.fixture
def tmp_ssh_dir(tmp_path):
    ssh_dir = tmp_path / ".ssh"
    ssh_dir.mkdir()
    return ssh_dir


def test_target_configure_with_no_data():
    """Test the /api/target/configure endpoint with no data."""
    response = client.put("/api/target/configure")
    assert response.status_code == 400
    print(response)
    assert response.json() == {"detail": "No data provided or malformed data."}


def test_target_configure_with_empty_data():
    """Test the /api/target/configure endpoint with empty data."""
    response = client.put("/api/target/configure", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_malformed_data():
    """Test the /api/target/configure endpoint with malformed data."""
    response = client.put("/api/target/configure", json={"hosts": "hosts"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_missing_hosts():
    """Test the /api/target/configure endpoint with missing hosts."""
    response = client.put(
        "/api/target/configure",
        json={"user": "user", "password": "password", "os": "os"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_missing_user():
    """Test the /api/target/configure endpoint with missing user."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "password": "password", "os": "os"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_missing_password():
    """Test the /api/target/configure endpoint with missing password."""
    response = client.put(
        "/api/target/configure", json={"hosts": "hosts", "user": "user", "os": "os"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_missing_os():
    """Test the /api/target/configure endpoint with missing os."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_empty_hosts():
    """Test the /api/target/configure endpoint with empty hosts."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_empty_user():
    """Test the /api/target/configure endpoint with empty user."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "user": "", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_empty_password():
    """Test the /api/target/configure endpoint with empty password."""
    response = client.put(
        "/api/target/configure", json={"hosts": "hosts", "user": "user", "password": ""}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_malformed_hosts():
    """Test the /api/target/configure endpoint with malformed hosts."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


def test_target_configure_with_unencrypted_data():
    """Test the /api/target/configure endpoint with unencrypted data."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "user": "user", "password": "password", "os": "os"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Missing hosts, user, password, OS, or malformed data."
    }


def test_target_configure_with_invalid_encrypted_data():
    """Test the /api/target/configure endpoint with invalid encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    hosts = encrypt("localhost", encryption_key.encode())
    user = encrypt("wrong_user", encryption_key.encode())
    password = encrypt("incorrect_password", encryption_key.encode())
    os = encrypt("Linux", encryption_key.encode())
    response = client.put(
        "/api/target/configure",
        json={"hosts": hosts, "user": user, "password": password, "os": os},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": 'Error: "Failed to configure target." on localhost.'
    }


def test_target_config_with_empty_encrypted_data():
    """Test the /api/target/configure endpoint with empty encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    hosts = encrypt("", encryption_key.encode())
    user = encrypt("", encryption_key.encode())
    password = encrypt("", encryption_key.encode())
    os = encrypt("", encryption_key.encode())
    response = client.put(
        "/api/target/configure",
        json={"hosts": hosts, "user": user, "password": password, "os": os},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or OS."}


@patch("subprocess.run")
@patch("pathlib.Path.home")
def test_target_config_with_correct_data(
    mock_pathlib_home, mock_subprocess_run, tmp_ssh_dir: Path
):
    """Test the /api/target/configure endpoint with correct data."""
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = b"mocked_key"
    mock_pathlib_home.return_value = tmp_ssh_dir.parent
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    hosts = encrypt("user_machine", encryption_key.encode())
    user = encrypt("user", encryption_key.encode())
    password = encrypt("password", encryption_key.encode())
    os = encrypt("Linux", encryption_key.encode())
    response = client.put(
        "/api/target/configure",
        json={"hosts": hosts, "user": user, "password": password, "os": os},
    )
    assert response.status_code == 200
    assert response.json() == "Configured target machines."
