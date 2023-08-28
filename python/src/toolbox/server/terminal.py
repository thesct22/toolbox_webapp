# This code was copied from the official documentation of terminado
# https://github.com/jupyter/terminado
# The code is licensed under the BSD 2-Clause License
# This permits the user to redistribute, modify and use the code
# in source and binary forms provided that the user
# retain the copyright in source code and binary redistributions.

"""A single common terminal for all websockets."""
from pathlib import Path

import terminado
from terminado import SingleTermManager, TermSocket
import tornado.ioloop
import tornado.web

# This demo requires tornado_xstatic and XStatic-term.js
import tornado_xstatic

STATIC_DIR = Path(terminado.__file__).parent / "_static"
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def run_loop(url: str, term_manager: SingleTermManager):
    """Run the tornado loop."""
    loop = tornado.ioloop.IOLoop.current()

    async def shutdown():
        await term_manager.shutdown()

    try:
        loop.start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT")
        loop.run_sync(shutdown)
    finally:
        loop.close()


class TerminalPageHandler(tornado.web.RequestHandler):
    """Renders the page that contains the terminal emulator."""

    def get(self):
        """Render the page."""
        return self.render(
            "termpage.html",
            static=self.static_url,
            xstatic=self.application.settings["xstatic_url"],
            ws_url_path="/websocket",
        )


def run_terminal(host: str = "localhost", port: int = 8765):
    """Run the terminal server."""
    term_manager = SingleTermManager(shell_command=["bash"])
    handlers = [
        (r"/websocket", TermSocket, {"term_manager": term_manager}),
        (r"/", TerminalPageHandler),
        (
            r"/xstatic/(.*)",
            tornado_xstatic.XStaticFileHandler,
            {"allowed_modules": ["termjs"]},
        ),
    ]
    app = tornado.web.Application(
        handlers,
        static_path=STATIC_DIR,
        template_path=TEMPLATE_DIR,
        xstatic_url=tornado_xstatic.url_maker("/xstatic/"),
    )
    app.listen(port, host)
    run_loop(f"http://{host}:{port}", term_manager)


if __name__ == "__main__":
    run_terminal("localhost", 8765)
