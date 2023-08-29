from unittest.mock import patch

from fastapi.testclient import TestClient
from toolbox.core.rsakey import encrypt
from toolbox.main import app

client = TestClient(app)

def test_get_homepage():
    """Test the / endpoint."""
    response = client.get("/")
    assert response.status_code == 200

def test_get_custom_playbooks():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/custom-playbook")
    assert response.status_code == 200

def test_get_configure_target():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/configure-target")
    assert response.status_code == 200

def test_get_code_editor():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/code-editor")
    assert response.status_code == 200

def test_get_terminal():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/terminal")
    assert response.status_code == 200

def test_get_instructions():
    """Test the /api/custom/playbooks endpoint."""
    response = client.get("/instructions")
    assert response.status_code == 200
