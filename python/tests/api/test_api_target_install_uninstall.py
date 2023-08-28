from unittest.mock import patch

from fastapi.testclient import TestClient
from toolbox.core.rsakey import encrypt
from toolbox.main import app

client = TestClient(app)


def test_install_target_with_no_data():
    """Test the /api/target/install endpoint with no data."""
    response = client.put("/api/target/install")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided or malformed data."}


def test_install_target_with_empty_data():
    """Test the /api/target/install endpoint with empty data."""
    response = client.put("/api/target/install", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_install_target_with_missing_hosts():
    """Test the /api/target/install endpoint with missing hosts."""
    data = {
        "user": "encrypted_user",
        "password": "encrypted_password",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_install_target_with_missing_user():
    """Test the /api/target/install endpoint with missing user."""
    data = {
        "hosts": "encrypted_hosts",
        "password": "encrypted_password",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_install_target_with_missing_password():
    """Test the /api/target/install endpoint with missing password."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_install_target_with_missing_tags():
    """Test the /api/target/install endpoint with missing tags."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "password": "encrypted_password",
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "No tags provided."}


def test_install_target_with_empty_tags():
    """Test the /api/target/install endpoint with empty tags."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "password": "encrypted_password",
        "tags": [],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "No tags provided."}


def test_install_target_with_wrong_encrypted_data():
    """Test the /api/target/install endpoint with wrong encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Failed to verify ansible credentials for host: hosts"
    }


def test_install_target_with_encrypted_empty_data():
    """Test the /api/target/install endpoint with encrypted empty data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("", encryption_key.encode()),
        "user": encrypt("", encryption_key.encode()),
        "password": encrypt("", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/install", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_install_target_with_correct_encrypted_data():
    """Test the /api/target/install endpoint with correct encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    with patch("toolbox.core.ansible.Ansible.verify_auth", return_value=None):
        with patch(
            "toolbox.core.ansible.Ansible.run_command",
            return_value="Installation successful",
        ):
            response = client.put("/api/target/install", json=data)
            assert response.status_code == 200
            assert response.json() == "Installation successful"


def test_uninstall_target_with_no_data():
    """Test the /api/target/uninstall endpoint with no data."""
    response = client.put("/api/target/uninstall")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided or malformed data."}


def test_uninstall_target_with_empty_data():
    """Test the /api/target/uninstall endpoint with empty data."""
    response = client.put("/api/target/uninstall", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided."}


def test_uninstall_target_with_missing_hosts():
    """Test the /api/target/uninstall endpoint with missing hosts."""
    data = {
        "user": "encrypted_user",
        "password": "encrypted_password",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_uninstall_target_with_missing_user():
    """Test the /api/target/uninstall endpoint with missing user."""
    data = {
        "hosts": "encrypted_hosts",
        "password": "encrypted_password",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_uninstall_target_with_missing_password():
    """Test the /api/target/uninstall endpoint with missing password."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_uninstall_target_with_missing_tags():
    """Test the /api/target/uninstall endpoint with missing tags."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "password": "encrypted_password",
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "No tags provided."}


def test_uninstall_target_with_empty_tags():
    """Test the /api/target/uninstall endpoint with empty tags."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "password": "encrypted_password",
        "tags": [],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "No tags provided."}


def test_uninstall_target_with_wrong_encrypted_data():
    """Test the /api/target/uninstall endpoint with wrong encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Failed to verify ansible credentials for host: hosts"
    }


def test_uninstall_target_with_encrypted_empty_data():
    """Test the /api/target/uninstall endpoint with encrypted empty data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("", encryption_key.encode()),
        "user": encrypt("", encryption_key.encode()),
        "password": encrypt("", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    response = client.put("/api/target/uninstall", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_uninstall_target_with_correct_encrypted_data():
    """Test the /api/target/uninstall endpoint with correct encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "tags": ["tag1", "tag2"],
    }
    with patch("toolbox.core.ansible.Ansible.verify_auth", return_value=None):
        with patch(
            "toolbox.core.ansible.Ansible.run_command",
            return_value="Uninstallation successful",
        ):
            response = client.put("/api/target/uninstall", json=data)
            assert response.status_code == 200
            assert response.json() == "Uninstallation successful"
