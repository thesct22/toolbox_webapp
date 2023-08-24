from pathlib import Path

from toolbox.server.main import run_server


def test_react_build_dir():
    """Check that the react build directory exists."""
    react_build_dir = Path(run_server.__code__.co_filename).parent.parent / "build"
    assert react_build_dir.exists()
    assert len(list(react_build_dir.iterdir())) > 0
