# Toolbox Webapp

## Installation

### Requirements

#### Operating System

* Linux (Ubuntu 20.04 LTS and up)

#### Python

* Python 3.9 and up

### Setup

Make sure you are in the `python` directory, which is the folder containing this README file.

```bash
cd python
```

Run the setup script.

```bash
./setup.sh
```

> Note: If you get a permission denied error, run `chmod +x setup.sh` and try again.
>
> Note: Powershell equivalent: `.\setup.ps1` is also provided. However, it is limited in capacity due to ansible not supporting Windows host machines. Ansible does support Windows target machines though.

Build the react static files and copy them and the ansible folder to the python source folder using this python script.

```bash
python ./tools/build.py
```

> Note: Make sure you run this from the `python` directory.

## Usage

Make sure you are in the `python` directory, which is the folder containing this README file.

```bash
cd python
```

### Running the webapp

Start uvicorn server.

```bash
poetry run python -m toolbox.main
```

### Enabling pre-commit hooks

> Note: Pre-commit is used for code quality and formatting. It is recommended to enable it.
>
> It runs code style checks and auto-formats code before committing and fails if there are any issues with the code, so you can fix them before committing.

```bash
poetry run pre-commit install
```

### Running pre-commit hooks manually

```bash
poetry run pre-commit run --all-files
```

> Note: This is automatically run when you commit changes.
