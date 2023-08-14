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
ENV DEBIAN_FRONTEND=noninteractive
# security best practice: create a non-root user with minimal permissions
RUN useradd -ms /bin/bash ansible && \
    apt update && \
    apt install -y sudo
RUN echo "ansible-password\nansible-password" | passwd ansible
RUN usermod -aG sudo ansible
RUN echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER ansible
WORKDIR /app
RUN sudo apt update && sudo apt install -y sshpass openssh-server
COPY --from=fastapi-build-stage /app/dist/*.whl ./
RUN pip install *.whl --target .
RUN rm *.whl
RUN sudo sed -i '/ansible ALL=(ALL) NOPASSWD:ALL/d' /etc/sudoers
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "${PATH}:/app:/app/bin"
EXPOSE 8000
EXPOSE 8765
WORKDIR /app/toolbox/ansible
ENTRYPOINT ["python", "-m", "toolbox.main", "--host", "0.0.0.0", "--port", "8000", "--terminal_host", "0.0.0.0", "--terminal_port", "8765"]
