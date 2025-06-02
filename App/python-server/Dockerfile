# Python 3.11 has vulnerability issues
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --upgrade pip
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#RUN pip install --upgrade passlib
# incompatibility issues with new bcrypt (revert to old version)
RUN pip install bcrypt==3.2.0
# Copy the rest of the application code into the container
COPY . .

# Install curl for debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
