from unittest.mock import MagicMock, patch

import pytest
from toolbox.helpers.find_free_port import find_free_port
from toolbox.server.terminal import run_terminal
from tornado.ioloop import IOLoop


@pytest.mark.parametrize(
    "host, port",
    [
        ("localhost", find_free_port("localhost")),
        ("localhost", find_free_port("localhost")),
    ],
)
def test_run_terminal_multiple_ports(host, port):
    mock_ioloop = MagicMock(spec=IOLoop)
    with patch(
        "toolbox.server.terminal.tornado.ioloop.IOLoop.current",
        return_value=mock_ioloop,
    ):
        run_terminal(host=host, port=port)
        mock_ioloop.start.assert_called_once()
