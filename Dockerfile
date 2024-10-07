# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run as non-root user
RUN useradd -m myuser
USER myuser

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Development stage
FROM base as development
RUN pip install --no-cache-dir pytest behave

# Production stage
FROM base as production
# Add any production-specific steps here