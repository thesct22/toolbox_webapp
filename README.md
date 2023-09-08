# Toolbox Webapp

[![CI](https://github.com/thesct22/toolbox_webapp/actions/workflows/ci.yml/badge.svg)](https://github.com/thesct22/toolbox_webapp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/thesct22/toolbox_webapp/graph/badge.svg?token=GYBFWGO7T0)](https://codecov.io/gh/thesct22/toolbox_webapp)
[![Docker-Container](https://img.shields.io/badge/docker-container-blue)](https://github.com/thesct22/toolbox_webapp/pkgs/container/toolbox)
[![Documentation](https://img.shields.io/badge/docs-gh--pages-blue)](https://thesct22.github.io/toolbox_webapp/)

[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-blue)](https://www.python.org/)
[![React Versions](https://img.shields.io/badge/react-17.0.2-blue)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/backend-fastapi-009688)](https://fastapi.tiangolo.com/)
[![Material UI](https://img.shields.io/badge/frontend-materialui-0081cb)](https://material-ui.com/)

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/lint-flake8-blue)](https://flake8.pycqa.org/)
[![isort](https://img.shields.io/badge/code%20style-isort-4c1)](https://pycqa.github.io/isort/)
[![codespell](https://img.shields.io/badge/spelling-codespell-lightgrey)](https://github.com/codespell-project/codespell)
[![pydocstyle](https://img.shields.io/badge/style-pydocstyle-blue)](https://www.pydocstyle.org/)
[![ESLint](https://img.shields.io/badge/frontend-eslint-blue)](https://eslint.org/)
[![Prettier](https://img.shields.io/badge/frontend-prettier-ff69b4)](https://prettier.io/)

[![Pytest](https://img.shields.io/badge/tests-pytest-green)](https://pytest.org)
[![Jest](https://img.shields.io/badge/frontend-jest-c21325)](https://jestjs.io/)

## About

Toolbox to install software on remote machines.

Works as UI wrapper for Ansible.

## Backend

The readme for the backend can be found [here](./python/README.md).

API documentation is publsihed on [github pages](https://thesct22.github.io/toolbox_webapp/).

## Frontend

The readme for the frontend can be found [here](./react-frontend/README.md).

## Pre-requisite

You need to have any one of the following:

* Docker
* Linux-based OS
* WSL2

## Docker Container

To execute the docker container, run the following command:

```bash
docker run -d -p 8000:8000 -p 8765:8765 --name toolbox ghcr.io/thesct22/toolbox:latest
```

To execute the docker container for testing the toolbox, run the following command:

```bash
docker run -d --name test1 ghcr.io/thesct22/toolbox-tester:latest
```

If you wish to run 1 more testing container, run the following command:

```bash
docker run -d --name test2 ghcr.io/thesct22/toolbox-tester:latest
```

To find the IP address of the container, run the following command:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

```

For example, the IP address of the tester containers can be found by running the following commands:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test1
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test2
```

Use these IP addresses to test the toolbox.

The username and password to use for these containers are:

| Username | Password |
| -------- | -------- |
| ansible  | ansible-password |

First Configure these targets using the `configure target` page (click on the gear icon on the navbar).

Once successfully configured, you can return to home page and select the tools you wish to install and provide the above username and password and IP address(es) and click on `Install` or `Uninstall` button.

The `Ping` button can be used to check if the target(s) are reachable.

To stop the containers, run the following command:

```bash
docker stop toolbox
docker stop test1
docker stop test2
```

> Note: Stop the container you wish to remove before deleting, delete it and create a new one.

To delete the containers, run the following command:

```bash
docker rm toolbox
docker rm test1
docker rm test2
```

> Note: Delete the container you wish to remove and create a new one.

To open the webapp go to: `http://localhost:8000`

## Executable

> Note: The executable is only available for Linux x86_64 and differnt from the above docker container.
> This can be used if you wish to not use docker.

To create the binary executable, run the following shell script in the root folder:

> assuming you the project is inside a Linux based OS.

```bash
./build_standalone.sh
```

> This might take a while, as nuitka needs to compile the whole project to form the executable.

To run the executable, run the following command:

```bash
cd toolbox
./main.bin
```

Note: The executable is only available for Linux x86_64.

To open the webapp go to: `http://localhost:8000`
