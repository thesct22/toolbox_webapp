from fastapi.testclient import TestClient
from toolbox.main import app

client = TestClient(app)


def test_install_tags():
    """Test the /api/install/tags endpoint."""
    response = client.get("/api/install/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert isinstance(item, dict)
        assert "title" in item
        assert isinstance(item["title"], str)
        assert "tags" in item
        assert isinstance(item["tags"], list)
        for tag in item["tags"]:
            assert isinstance(tag, str)


def test_uninstall_tags():
    """Test the /api/uninstall/tags endpoint."""
    response = client.get("/api/uninstall/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert isinstance(item, dict)
        assert "title" in item
        assert isinstance(item["title"], str)
        assert "tags" in item
        assert isinstance(item["tags"], list)
        for tag in item["tags"]:
            assert isinstance(tag, str)
