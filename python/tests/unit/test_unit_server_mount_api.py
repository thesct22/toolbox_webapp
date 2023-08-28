from unittest.mock import MagicMock

from fastapi import FastAPI
import pytest
from toolbox.server.mount_api import mount_api


@pytest.fixture
def mock_install_endpoints():
    return MagicMock()


@pytest.fixture
def mock_uninstall_endpoints():
    return MagicMock()


@pytest.fixture
def mock_target_endpoints():
    return MagicMock()


@pytest.fixture
def mock_editor_endpoints():
    return MagicMock()


@pytest.fixture
def mock_custom_endpoints():
    return MagicMock()


def test_mount_api_with_endpoints(
    mock_install_endpoints,
    mock_uninstall_endpoints,
    mock_target_endpoints,
    mock_editor_endpoints,
    mock_custom_endpoints,
):
    app = FastAPI()

    mock_install_endpoints.return_value = "install_endpoint_mock"
    mock_uninstall_endpoints.return_value = "uninstall_endpoint_mock"
    mock_target_endpoints.return_value = "target_endpoint_mock"
    mock_editor_endpoints.return_value = "editor_endpoint_mock"
    mock_custom_endpoints.return_value = "custom_endpoint_mock"

    result_app = mount_api(app)

    assert result_app == app
    assert app.routes[0].path == "/openapi.json"
    assert app.routes[1].path == "/docs"
    assert app.routes[2].path == "/docs/oauth2-redirect"
    assert app.routes[3].path == "/redoc"
    assert app.routes[4].path == "/api"
    assert app.routes[5].path == "/api/health"
    assert app.routes[6].path == "/api/public_key"
    assert app.routes[7].path == "/api/install/tags"
    assert app.routes[8].path == "/api/install"
    assert app.routes[9].path == "/api/uninstall/tags"
    assert app.routes[10].path == "/api/uninstall"
    assert app.routes[11].path == "/api/target/configure"
    assert app.routes[12].path == "/api/target/ping"
    assert app.routes[13].path == "/api/target/install"
    assert app.routes[14].path == "/api/target/uninstall"
    assert app.routes[15].path == "/api/target"
    assert app.routes[16].path == "/api/editor/files"
    assert app.routes[17].path == "/api/editor/file/read"
    assert app.routes[18].path == "/api/editor/file/write"
    assert app.routes[19].path == "/api/editor/file/create"
    assert app.routes[20].path == "/api/editor/file/delete"
    assert app.routes[21].path == "/api/editor/file/rename"
    assert app.routes[22].path == "/api/editor/folder/create"
    assert app.routes[23].path == "/api/editor/folder/delete"
    assert app.routes[24].path == "/api/editor/folder/delete/confirmed"
    assert app.routes[25].path == "/api/editor/folder/rename"
    assert app.routes[26].path == "/api/editor"
    assert app.routes[27].path == "/api/custom/playbooks"
    assert app.routes[28].path == "/api/custom/inventories"
    assert app.routes[29].path == "/api/custom/run"
    assert app.routes[30].path == "/api/custom"


def test_mount_api_without_endpoints():
    app = FastAPI()

    result_app = mount_api(app)

    assert result_app == app
    assert app.routes[0].path == "/openapi.json"
    assert app.routes[1].path == "/docs"
    assert app.routes[2].path == "/docs/oauth2-redirect"
    assert app.routes[3].path == "/redoc"
    assert app.routes[4].path == "/api"
    assert app.routes[5].path == "/api/health"
    assert app.routes[6].path == "/api/public_key"
    assert app.routes[7].path == "/api/install/tags"
    assert app.routes[8].path == "/api/install"
    assert app.routes[9].path == "/api/uninstall/tags"
    assert app.routes[10].path == "/api/uninstall"
    assert app.routes[11].path == "/api/target/configure"
    assert app.routes[12].path == "/api/target/ping"
    assert app.routes[13].path == "/api/target/install"
    assert app.routes[14].path == "/api/target/uninstall"
    assert app.routes[15].path == "/api/target"
    assert app.routes[16].path == "/api/editor/files"
    assert app.routes[17].path == "/api/editor/file/read"
    assert app.routes[18].path == "/api/editor/file/write"
    assert app.routes[19].path == "/api/editor/file/create"
    assert app.routes[20].path == "/api/editor/file/delete"
    assert app.routes[21].path == "/api/editor/file/rename"
    assert app.routes[22].path == "/api/editor/folder/create"
    assert app.routes[23].path == "/api/editor/folder/delete"
    assert app.routes[24].path == "/api/editor/folder/delete/confirmed"
    assert app.routes[25].path == "/api/editor/folder/rename"
    assert app.routes[26].path == "/api/editor"
    assert app.routes[27].path == "/api/custom/playbooks"
    assert app.routes[28].path == "/api/custom/inventories"
    assert app.routes[29].path == "/api/custom/run"
    assert app.routes[30].path == "/api/custom"


def test_if_mount_api_returns_fastapi_app():
    app = FastAPI()

    result_app = mount_api(app)

    assert result_app == app
