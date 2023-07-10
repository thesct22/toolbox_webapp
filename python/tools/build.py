"""This script builds the react static files and copies the dist and the ansible folders to python src."""
from pathlib import Path
import shutil
import subprocess


def build():
    """Build the react static files and copies the dist and the ansible folders to python src."""
    # check if npm is installed
    if shutil.which("npm") is None:
        raise Exception("npm is not installed")

    # build react static files
    try:
        subprocess.run(["npm", "run", "build"], cwd="react", check=True)
    except subprocess.CalledProcessError as e:
        raise Exception("npm build failed") from e

    # copy dist and ansible folders to python src
    react_dist = Path(__file__).parent.parent.parent / "react-frontends" / "build"
    ansible = Path(__file__).parent.parent.parent / "ansible"
    python_src = Path(__file__).parent.parent / "src" / "toolbox"
    shutil.rmtree(python_src / "build", ignore_errors=True)
    shutil.rmtree(python_src / "ansible", ignore_errors=True)
    shutil.copytree(react_dist, python_src / "build")
    shutil.copytree(ansible, python_src / "ansible")


if __name__ == "__main__":
    build()
