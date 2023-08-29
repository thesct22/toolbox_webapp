from pathlib import Path
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pytest
from toolbox.server.mount_frontend import mount_frontend


@pytest.fixture
def mock_app():
    return Mock(spec=FastAPI)


@pytest.fixture
def mock_react_build_dir(tmp_path: Path):
    tmp_path = tmp_path / "react_build_dir"
    tmp_path.mkdir()
    (tmp_path / "static").mkdir()
    return tmp_path


def test_mount_frontend(mock_app, mock_react_build_dir):
    result_app = mount_frontend(mock_app, mock_react_build_dir)

    assert result_app == mock_app
    assert mock_app.mount.call_count == 1
    assert mock_app.mount.call_args_list[0][0][0] == "/"
    assert isinstance(mock_app.mount.call_args_list[0][0][1], StaticFiles)
    assert mock_app.mount.call_args_list[0][1] == {"name": "static"}

