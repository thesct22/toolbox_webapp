"""APIs for implementing a websocket terminal."""
import os
import select
import sys
import termios
import tty

from fastapi import FastAPI, WebSocket


def terminal_endpoints(app: FastAPI) -> FastAPI:
    """
    Aggregate of all the /api/terminal endpoints.

    Args:
        app (FastAPI): The FastAPI app.
    Returns:
        FastAPI: The FastAPI app.
    """

    @app.websocket("/api/terminal")
    async def terminal(websocket: WebSocket) -> None:
        """Run a terminal."""
        await websocket.accept()
        master, slave = os.openpty()
        old_term_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(master)
            while True:
                rlist, _, _ = select.select([sys.stdin, master], [], [])
                for src in rlist:
                    if src == master:
                        data = os.read(master, 1024)
                        await websocket.send_text(data.decode())
                    elif src == websocket:
                        data = await websocket.receive_text()
                        os.write(master, data.encode())
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_term_settings)
            os.close(master)
            os.close(slave)
            await websocket.close()

    return app
