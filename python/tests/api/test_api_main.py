from fastapi.testclient import TestClient
from toolbox.main import build_app

client = TestClient(build_app())


def test_api_endpoint():
    """Test the /api endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == "This is the toolbox server API endpoint."


def test_health():
    """Test the health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == "OK"


def test_404():
    """Test the 404 endpoint."""
    response = client.get("/api/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_RSA_public_key():
    """Test the /api/public_key endpoint."""
    response = client.get("/api/public_key")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "public_key" in response.json()
    assert isinstance(response.json()["public_key"], str)
    assert "-----BEGIN PUBLIC KEY-----" in response.json()["public_key"]
    assert "-----END PUBLIC KEY-----" in response.json()["public_key"]


def test_terminal_url():
    """Test the /api/terminal/url endpoint."""
    response = client.get("/api/terminal/url")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "url" in response.json()
    assert isinstance(response.json()["url"], str)
    assert "http://" in response.json()["url"]
    assert ":8765" in response.json()["url"]
    assert "localhost" in response.json()["url"]
