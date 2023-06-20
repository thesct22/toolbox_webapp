# remove old virtual environment and cache if present
if (Test-Path -Path ".venv") {
    Remove-Item -Recurse -Force .venv
}
if (Test-Path -Path ".poetry/poetry_cache") {
    Remove-Item -Recurse -Force .poetry_cache
}

# install pywin32
python -m pip install --upgrade pip setuptools pywin32 pipx

# create a new virtual environment
python -m venv .venv

# install poetry
pipx install poetry

# install all dependencies
poetry install --with test,doc,code_style,build