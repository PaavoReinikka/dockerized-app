FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the test files into the container
COPY ./tests /app/tests

COPY ./pyproject.toml /app/pyproject.toml
COPY ./pytest.ini /app/pytest.ini

# Add python-server to PYTHONPATH
ENV PYTHONPATH="/app/python-server:$PYTHONPATH"

# Install dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync

RUN uv add pip
RUN uv run pip install --upgrade httpx

# Set the default command to run pytest
CMD ["uv", "run", "pytest", "tests"]