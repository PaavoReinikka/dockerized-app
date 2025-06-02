FROM ollama/ollama

# I will clean this up later (Paavo)
# Set working directory
WORKDIR /app

# Copy the script to the docker image
COPY ./user-chat/run.sh /run.sh

COPY ./user-chat/gradio_dashboard.py /app/gradio_dashboard.py

COPY ./user-chat/.env.development /app/.env.development

COPY ./user-chat/pyproject.toml /app/pyproject.toml

# Install dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates python3

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer (then remove it)
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set environment variables for Gradio server
ENV GRADIO_SERVER_NAME="0.0.0.0"

#RUN pip install --no-cache-dir -r requirements.txt
RUN uv sync

# Ensure the script is executable
RUN chmod +x /run.sh

ENTRYPOINT ["/bin/bash", "/run.sh"]