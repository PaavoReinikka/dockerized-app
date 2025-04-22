FROM ollama/ollama

# Set working directory
WORKDIR /app

# Copy all files from the context to the image, excluding those in .dockerignore
COPY ./chat-engine/ /app/

# Install dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates python3

# Download the latest installer for uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

ENV GRADIO_SERVER_NAME="0.0.0.0"

RUN uv sync

# Ensure the script is executable
RUN chmod +x /app/run.sh

ENTRYPOINT ["/bin/bash", "/app/run.sh"]