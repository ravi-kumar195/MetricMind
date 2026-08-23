# Use an official lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files & buffer output for real-time logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy dependency definition first (enables Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining project files
COPY . .

# Default command executed when container starts
CMD ["python", "data_processor.py"]