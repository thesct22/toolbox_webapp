# Path: python\setup.ps1

# remove old virtual environment and cache
Remove-Item -Recurse -Force .venv
Remove-Item -Recurse -Force .poetry_cache

# install pipx and setuptools, and upfate pip
python -m pip install --upgrade pip setuptools pipx

# create a new virtual environment
python -m venv .venv

# install poetry
pipx install poetry

# install all dependencies
poetry install --with test,doc,code_style,build
