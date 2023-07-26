"""Run the server."""
import argparse
from pathlib import Path

from toolbox.server.main import run_server

if __name__ == "__main__":
    """Run the server."""
    parser = argparse.ArgumentParser(description="Run the server.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to run the server on.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on.",
    )
    args = parser.parse_args()

    run_server(
        react_build_dir=Path(__file__).parent / "build", host=args.host, port=args.port
    )
