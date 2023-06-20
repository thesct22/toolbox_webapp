"""Run the server."""

from pathlib import Path

from toolbox.server.main import run_server

if __name__ == "__main__":
    """Run the server."""
    run_server(
        react_build_dir=Path(__file__).parent / "build", host="localhost", port=8000
    )
