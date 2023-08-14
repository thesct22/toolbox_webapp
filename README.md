# Toolbox Webapp

## Docker Container

Login to ghcr.io to be able to pull this image

```bash
docker login ghcr.io
```

Username is your GitHub username

To generate password, go to:

`https://github.com/settings/tokens/new` and check the "read:packages" box. Then click on Generate Token button in the end.

Copy the token generated and paste this as the password. The token begins with `ghp_`.

You should see a message saying login succeeded.

To execute the docker container, run the following command:

```bash
docker run -d -p 8000:8000 -p 8765:8765 ghcr.io/thesct22/toolbox:lastest
```

To stop the container, run the following command:

```bash
docker stop <container-id>
```

To find the container id, run the following command:

```bash
docker ps
```

You can find the ID in the first column.

To delete the container, run the following command:

```bash
docker rm <container-id>
```

To open the webapp go to: `http://localhost:8000`

## Executable

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
