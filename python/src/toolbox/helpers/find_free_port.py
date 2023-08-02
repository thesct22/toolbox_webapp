"""Helper function to find a free port on the local machine."""
import socket
from typing import Optional


def find_free_port(host: str = "localhost") -> Optional[int]:
    """Find a free port on the local machine.

    Args:
        host: Host to check for free ports on.

    Returns:
        A free port on the local machine.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        sock.listen(1)
        return sock.getsockname()[1]
