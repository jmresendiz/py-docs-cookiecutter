# MkDocs Dockerfile for {{ cookiecutter.project_name }}
# Base image with Python for running MkDocs

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /docs

# Install MkDocs and plugins
RUN pip install --no-cache-dir \
    mkdocs==1.6.1 \
    mkdocs-material==9.5.47 \
    pymdown-extensions==10.12

# Expose port for MkDocs dev server
EXPOSE 8000

# Default command
CMD ["mkdocs", "serve", "--help"]

