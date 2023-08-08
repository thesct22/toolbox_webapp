"""Run the server."""
import argparse
import concurrent.futures
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolbox.server.main import run_server
from toolbox.server.mount_api import mount_api
from toolbox.server.mount_frontend import mount_frontend
from toolbox.server.terminal import run_terminal
import webview

app = FastAPI(title="Toolbox Webapp")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app = mount_api(app)
app = mount_frontend(app, react_build_dir=Path(__file__).parent / "build")

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

    # run both the servers in parallel

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        try:
            server_thread = executor.submit(run_server, app, args.host, args.port)
            terminal_thread = executor.submit(
                run_terminal, args.terminal_host, args.terminal_port
            )
            webview_thread = executor.submit(
                webview.create_window,
                "Toolbox",
                f"http://{args.host}:{args.port}",
                width=800,
                height=600,
            )

            # Wait for all threads to complete
            threads = concurrent.futures.wait(
                [server_thread, terminal_thread, webview_thread]
            )

        except KeyboardInterrupt:
            print(" Shutting down on SIGINT")
        finally:
            executor.shutdown(wait=False)
