# Use the official Python image from the Docker Hub
FROM python:3.11.9-slim

# Clean up apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Poetry
RUN python -m pip install --upgrade pip
RUN pip install poetry==1.7.1

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

COPY .env.deploy /app/.env

# Copy the rest of the project files
COPY . /app

# Create cache directories

# Expose port 
EXPOSE 8888

# Command to run the application
# CMD ["poetry", "run", "uvicorn", "eoy.collator:app", "--host", "0.0.0.0", "--port", "8888"]
