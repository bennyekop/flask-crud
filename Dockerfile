# Use an official Python runtime as a parent image

FROM python:3.9-slim-buster


# Set the working directory in the container

WORKDIR /app


# Set environment variable to prevent interactive prompts during apt-get operations

ENV DEBIAN_FRONTEND=noninteractive


# Explicitly configure APT sources to include main, contrib, and non-free components.

# This ensures that all necessary dependencies can be found for Debian Buster.

RUN echo "deb http://deb.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list \

    && echo "deb http://deb.debian.org/debian buster-updates main contrib non-free" >> /etc/apt/sources.list \

    && echo "deb http://security.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list


# Update package lists and install system dependencies.

# build-essential: Provides compilers (gcc, g++), make, etc. needed for C extensions.

# pkg-config: Used to find libraries for compilation.

# default-libmysqlclient-dev: Generic MySQL client development headers needed by Flask-MySQLdb.

RUN apt-get update \

    && apt-get install -y --no-install-recommends \

    build-essential \

    pkg-config \

    default-libmysqlclient-dev


# Clean up apt cache to keep the image size down

RUN rm -rf /var/lib/apt/lists/*


# Install any Python packages specified in requirements.txt

# Copy only requirements.txt first to leverage Docker's build cache.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code into the container's /app directory

COPY . .


# Expose port 5000, which is the default port for Flask development server

EXPOSE 5000


# Command to run the Flask application when the container starts

CMD ["python", "app.py"]
