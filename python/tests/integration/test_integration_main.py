import subprocess
import sys
import time
from unittest.mock import MagicMock, patch

import requests
from toolbox.helpers.find_free_port import find_free_port
from toolbox.main import arg_parser, run_webapp


def test_server_with_all_paramters():
    """Test the server with all parameters."""
    host = "localhost"
    port = find_free_port(host)
    terminal_host = "localhost"
    terminal_port = find_free_port(terminal_host)
    url = f"http://{host}:{port}/api/health"
    terminal_url = f"http://{terminal_host}:{terminal_port}/"
    server_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "toolbox.main",
            "--host",
            host,
            "--port",
            str(port),
            "--terminal_host",
            terminal_host,
            "--terminal_port",
            str(terminal_port),
        ]
    )
    time.sleep(10)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == "OK"
    terminal_response = requests.get(terminal_url)
    assert terminal_response.status_code == 200
    server_process.terminate()


def test_arg_parser():
    """Test the arg_parser."""
    with patch("sys.argv", ["main.py"]):
        args = arg_parser()
        assert args.host == "localhost"
        assert args.port == 8000
        assert args.terminal_host == "localhost"
        assert args.terminal_port == 8765


def test_arg_parser_with_all_parameters():
    """Test the arg_parser with all parameters."""
    port = find_free_port("localhost")
    terminal_port = find_free_port("localhost")
    with patch(
        "sys.argv",
        [
            "main.py",
            "--host",
            "localhost",
            "--port",
            str(port),
            "--terminal_host",
            "localhost",
            "--terminal_port",
            str(terminal_port),
        ],
    ):
        args = arg_parser()
        assert args.host == "localhost"
        assert args.port == port
        assert args.terminal_host == "localhost"
        assert args.terminal_port == terminal_port


@patch("multiprocessing.Process")
@patch("webview.create_window")
def test_run_webapp(mock_create_window, mock_Process):
    args = MagicMock()
    mock_server_process = MagicMock()
    mock_terminal_process = MagicMock()
    mock_Process.side_effect = [mock_server_process, mock_terminal_process]

    run_webapp(args)

    mock_server_process.start.assert_called_once()
    mock_terminal_process.start.assert_called_once()
    mock_create_window.assert_called_once_with(
        "Toolbox", f"http://{args.host}:{args.port}", width=800, height=600
    )
    mock_server_process.join.assert_called_once()
    mock_terminal_process.join.assert_called_once()
