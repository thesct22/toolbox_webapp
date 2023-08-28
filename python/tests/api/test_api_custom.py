from unittest.mock import patch

from fastapi.testclient import TestClient
from toolbox.core.rsakey import encrypt
from toolbox.main import app

client = TestClient(app)


def test_get_custom_playbooks():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/api/custom/playbooks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_custom_inventory():
    """Test the /api/custom/inventories endpoint."""
    response = client.get("/api/custom/inventories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_run_custom_with_no_data():
    """Test the /api/custom/run endpoint with empty data."""
    response = client.put("/api/custom/run")
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided or malformed data."}


def test_run_custom_with_empty_data():
    """Test the /api/custom/run endpoint with missing data."""
    response = client.put("/api/custom/run", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_missing_hosts():
    """Test the /api/custom/run endpoint with missing hosts."""
    data = {
        "user": "encrypted_user",
        "password": "encrypted_password",
        "playbook": "encrypted_playbook",
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_missing_user():
    """Test the /api/custom/run endpoint with missing user."""
    data = {
        "hosts": "encrypted_hosts",
        "password": "encrypted_password",
        "playbook": "encrypted_playbook",
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_missing_password():
    """Test the /api/custom/run endpoint with missing password."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "playbook": "encrypted_playbook",
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_missing_playbook():
    """Test the /api/custom/run endpoint with missing playbook."""
    data = {
        "hosts": "encrypted_hosts",
        "user": "encrypted_user",
        "password": "encrypted_password",
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_empty_data_fields():
    """Test the /api/custom/run endpoint with empty data fields."""
    data = {
        "hosts": "",
        "user": "",
        "password": "",
        "playbook": "",
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user, password or playbook."}


def test_run_custom_with_wrong_encrypted_data():
    """Test the /api/custom/run endpoint with wrong encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "playbook": encrypt("playbook", encryption_key.encode()),
    }
    response = client.put("/api/custom/run", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Failed to verify ansible credentials for host: hosts"
    }


def test_run_custom_with_correct_encryption_mocked():
    """Test the /api/custom/run endpoint with wrong encrypted hosts."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "playbook": encrypt("playbook", encryption_key.encode()),
    }
    with patch("toolbox.core.ansible.Ansible.verify_auth", return_value=None):
        with patch(
            "toolbox.core.ansible.Ansible.run_command",
            return_value="Ran Ansible successfully",
        ):
            response = client.put("/api/custom/run", json=data)
            assert response.status_code == 200
            assert response.json() == "Ran Ansible successfully"


def test_run_custom_with_non_integer_verbosity():
    """Test the /api/custom/run endpoint with non-integer verbosity."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "playbook": encrypt("playbook", encryption_key.encode()),
        "verbosity": "non-integer",
    }
    with patch("toolbox.core.ansible.Ansible.verify_auth", return_value=None):
        with patch(
            "toolbox.core.ansible.Ansible.run_command",
            return_value="Ran Ansible successfully",
        ):
            response = client.put("/api/custom/run", json=data)
            assert response.status_code == 200
            assert response.json() == "Ran Ansible successfully"


def test_run_custom_with_all_data():
    """Test the /api/custom/run endpoint with all data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    data = {
        "hosts": encrypt("hosts", encryption_key.encode()),
        "user": encrypt("user", encryption_key.encode()),
        "password": encrypt("password", encryption_key.encode()),
        "playbook": encrypt("playbook", encryption_key.encode()),
        "extra_vars": encrypt(
            '[{"key": "key", "value": "value"}]', encryption_key.encode()
        ),
        "tags": encrypt("tags", encryption_key.encode()),
        "extra_args": encrypt("extra_args", encryption_key.encode()),
        "verbosity": 1,
    }
    with patch("toolbox.core.ansible.Ansible.verify_auth", return_value=None):
        with patch(
            "toolbox.core.ansible.Ansible.run_command",
            return_value="Ran Ansible successfully",
        ):
            response = client.put("/api/custom/run", json=data)
            assert response.status_code == 200
            assert response.json() == "Ran Ansible successfully"
