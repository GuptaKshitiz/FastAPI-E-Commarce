# Dockerfile for the Celery Worker service

# 1. Base image (using the requested Python 3.10)
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory in the container
WORKDIR /usr/src/app

# 4. Copy requirements file and install dependencies
# We assume you have a requirements.txt with: celery, redis, etc.
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# 5. Copy the rest of the application code
COPY . .
