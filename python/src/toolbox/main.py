"""Main entrypoint for the toolbox webapp."""
import argparse
import multiprocessing
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolbox.server.main import run_server
from toolbox.server.mount_api import mount_api
from toolbox.server.mount_frontend import mount_frontend
from toolbox.server.terminal import run_terminal
import webview


def build_app(terminal_host: str = "localhost", terminal_port: int = 8765) -> FastAPI:
    """Build the FastAPI app."""
    app = FastAPI(title="Toolbox Webapp")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app = mount_api(app, terminal_host, terminal_port)
    app = mount_frontend(app, react_build_dir=Path(__file__).parent / "build")
    return app


def arg_parser():
    """Parse the arguments."""
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
    parser.add_argument(
        "--terminal_host",
        type=str,
        default="localhost",
        help="Host to run the terminal on.",
    )
    parser.add_argument(
        "--terminal_port",
        type=int,
        default=8765,
        help="Port to run the terminal on.",
    )
    args = parser.parse_args()
    return args


def run_server_app(app, host, port):
    """Run the FastAPI server."""
    run_server(app, host, port)


def run_terminal_app(terminal_host, terminal_port):
    """Run the terminal server."""
    run_terminal(terminal_host, terminal_port)


def run_webapp(args):
    """Run the webapp."""
    app = build_app(args.terminal_host, args.terminal_port)
    server_process = multiprocessing.Process(
        target=run_server_app, args=(app, args.host, args.port)
    )
    terminal_process = multiprocessing.Process(
        target=run_terminal_app, args=(args.terminal_host, args.terminal_port)
    )

    processes = [server_process, terminal_process]

    try:
        for process in processes:
            process.start()

        webview.create_window(
            "Toolbox",
            f"http://{args.host}:{args.port}",
            width=800,
            height=600,
        )

        for process in processes:
            process.join()

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        for process in processes:
            process.terminate()
            process.join()


if __name__ == "__main__":
    args = arg_parser()
    run_webapp(args)
