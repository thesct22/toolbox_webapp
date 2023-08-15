# Toolbox Webapp

## Docker Container

To execute the docker container, run the following command:

```bash
docker run -d -p 8000:8000 -p 8765:8765 ghcr.io/thesct22/toolbox:lastest --name toolbox
```

To execute the docker container for testing the toolbox, run the following command:

```bash
docker run -d ghcr.io/thesct22/toolbox-tester:lastest --name test1
```

If you wish to run 1 more testing container, run the following command:

```bash
docker run -d ghcr.io/thesct22/toolbox-tester:lastest --name test2
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
> Contact me if you wish to receive the link to download the executable.

To run the executable, run the following command:

```bash
cd toolbox-webapp
./main.bin
```

Note: The executable is only available for Linux x86_64.

To open the webapp go to: `http://localhost:8000`

## Backend

The readme for the backend can be found [here](./python/README.md).

## Frontend

The readme for the frontend can be found [here](./react-frontend/README.md).
