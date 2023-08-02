# Build the React Distribution folder
FROM node:lts-alpine as react-build-stage
WORKDIR /app
COPY react-frontend/package*.json ./
RUN npm ci
COPY react-frontend/ ./
RUN npm run build

# Build the FastAPI server
FROM python:3.11-slim as fastapi-build-stage
WORKDIR /app
COPY python/pyproject.toml python/poetry.lock python/poetry.toml python/README.md ./
COPY python/src/ ./src/
RUN pip install --upgrade pip setuptools wheel && \
    pip install poetry
RUN poetry install --with build
COPY ansible ./src/toolbox/ansible
COPY --from=react-build-stage /app/build ./src/toolbox/build
RUN poetry build

# Production image
FROM python:3.11-slim
WORKDIR /app
RUN apt update && apt install -y sshpass openssh-server
COPY --from=fastapi-build-stage /app/dist/*.whl ./
RUN pip install *.whl
EXPOSE 8000
ENTRYPOINT ["python", "-m", "toolbox.main", "--host", "0.0.0.0", "--port", "8000"]
