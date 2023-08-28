from unittest.mock import patch

from fastapi import FastAPI
import pytest
from toolbox.server.main import run_server


@patch("toolbox.server.main.uvicorn.run")
def test_run_server(mock_uvicorn_run):
    app = FastAPI()
    run_server(app)

    mock_uvicorn_run.assert_called_once_with(app, host="localhost", port=8000)


@pytest.mark.parametrize(
    "host, port",
    [
        ("localhost", 8000),
        ("localhost", 8001),
        ("localhost", 8002),
        ("localhost", 8003),
    ],
)
@patch("toolbox.server.main.uvicorn.run")
def test_run_server_multiple_ports(mock_uvicorn_run, host, port):
    app = FastAPI()
    run_server(app, host=host, port=port)

    mock_uvicorn_run.assert_called_once_with(app, host=host, port=port)
