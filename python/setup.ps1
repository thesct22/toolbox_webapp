# remove old virtual environment and cache if present
if (Test-Path -Path ".venv") {
    Remove-Item -Recurse -Force .venv
}
if (Test-Path -Path ".poetry/poetry_cache") {
    Remove-Item -Recurse -Force .poetry_cache
}

# install pywin32
python -m pip install pywin32

# create a new virtual environment
python -m venv .venv

# update pip and install setuptools
.venv\Scripts\python -m pip install --upgrade pip setuptools

# install poetry
.venv\Scripts\python -m pip install poetry

# install all dependencies
.venv\Scripts\poetry install --with test,doc,code_style,build