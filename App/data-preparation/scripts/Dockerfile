# python:3.10-slim has security issues, so we changed to python:3.13-slim
FROM python:3.13-slim 

# Install required system packages (libpq-dev for psycopg2, vim for Q&D edits)
# and gnumeric for Excel file handling
RUN apt-get update && apt-get install -y \
    curl \
    gnumeric \
    libpq-dev \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies using pip
RUN pip install --no-cache-dir \
    pandas \
    psycopg2-binary

# Set the working directory
WORKDIR /scripts

# Copy the scripts into the container
COPY . /scripts

# Ensure all .sh scripts are executable
RUN chmod +x /scripts/*.sh

# Default command (can be overridden in docker-compose)
CMD ["bash"]