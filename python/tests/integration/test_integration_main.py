import subprocess
import time

import requests
from toolbox.helpers.find_free_port import find_free_port


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
