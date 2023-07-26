# Path: python\setup.sh

# remove old virtual environment and cache
rm -rf .venv
rm -rf .poetry_cache

# install pipx and setuptools, and upfate pip
python3.11 -m pip install --upgrade pip setuptools pipx

# create a new virtual environment
python3.11 -m venv .venv

# install poetry
pipx install poetry

# ensure path is set correctly
pipx ensurepath

# install all dependencies
poetry install --with test,doc,code_style,build
