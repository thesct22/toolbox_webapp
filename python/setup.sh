# Path: python\setup.sh

# remove old virtual environment and cache
rm -rf .venv
rm -rf .poetry_cache

# create a new virtual environment
python3.11 -m venv .venv

# update pip and install setuptools
.venv/bin/python -m pip install --upgrade pip setuptools

# install poetry
.venv/bin/python -m pip install poetry

# install all dependencies
.venv/bin/poetry install --with test,doc,code_style,build
