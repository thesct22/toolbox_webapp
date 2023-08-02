from fastapi.testclient import TestClient
from toolbox.core.rsakey import encrypt
from toolbox.main import app

client = TestClient(app)


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
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_malformed_data():
    """Test the /api/target/configure endpoint with malformed data."""
    response = client.put("/api/target/configure", json={"hosts": "hosts"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_missing_hosts():
    """Test the /api/target/configure endpoint with missing hosts."""
    response = client.put(
        "/api/target/configure", json={"user": "user", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_missing_user():
    """Test the /api/target/configure endpoint with missing user."""
    response = client.put(
        "/api/target/configure", json={"hosts": "hosts", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_missing_password():
    """Test the /api/target/configure endpoint with missing password."""
    response = client.put(
        "/api/target/configure", json={"hosts": "hosts", "user": "user"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_empty_hosts():
    """Test the /api/target/configure endpoint with empty hosts."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_empty_user():
    """Test the /api/target/configure endpoint with empty user."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "user": "", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_empty_password():
    """Test the /api/target/configure endpoint with empty password."""
    response = client.put(
        "/api/target/configure", json={"hosts": "hosts", "user": "user", "password": ""}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_malformed_hosts():
    """Test the /api/target/configure endpoint with malformed hosts."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing hosts, user or password."}


def test_target_configure_with_unencrypted_data():
    """Test the /api/target/configure endpoint with unencrypted data."""
    response = client.put(
        "/api/target/configure",
        json={"hosts": "hosts", "user": "user", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Missing hosts, user or password, or malformed data."
    }


def test_target_configure_with_encrypted_data():
    """Test the /api/target/configure endpoint with encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    hosts = encrypt("localhost", encryption_key.encode())
    user = encrypt("sharath", encryption_key.encode())
    password = encrypt("253362", encryption_key.encode())
    response = client.put(
        "/api/target/configure",
        json={"hosts": hosts, "user": user, "password": password},
    )
    assert response.status_code == 200
    assert response.json() == "Configured target machines."


def test_target_configure_with_invalid_encrypted_data():
    """Test the /api/target/configure endpoint with invalid encrypted data."""
    encryption_key: str = client.get("/api/public_key").json()["public_key"]
    hosts = encrypt("localhost", encryption_key.encode())
    user = encrypt("wrong_user", encryption_key.encode())
    password = encrypt("incorrect_password", encryption_key.encode())
    response = client.put(
        "/api/target/configure",
        json={"hosts": hosts, "user": user, "password": password},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": 'Error: "Failed to configure target." on localhost.'
    }
