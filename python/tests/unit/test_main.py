from pathlib import Path
import subprocess
import time

from fastapi.testclient import TestClient
import requests
from toolbox.helpers.find_free_port import find_free_port
from toolbox.main import app
from toolbox.server.main import run_server

client = TestClient(app)


def test_server():
    """Test the server."""
    host = "localhost"
    port = find_free_port(host)
    url = f"http://{host}:{port}/api/health"
    server_process = subprocess.Popen(
        ["python", "-m", "toolbox.main", "--host", host, "--port", str(port)]
    )
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == "OK"
    server_process.terminate()


def test_server_default_parameters():
    """Test the server with default parameters."""
    host = "localhost"
    port = 8000
    url = f"http://{host}:{port}/api/health"
    server_process = subprocess.Popen(["python", "-m", "toolbox.main"])
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == "OK"
    server_process.terminate()


def test_react_build_dir():
    """Check that the react build directory exists."""
    react_build_dir = Path(run_server.__code__.co_filename).parent.parent / "build"
    assert react_build_dir.exists()
    assert len(list(react_build_dir.iterdir())) > 0


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
