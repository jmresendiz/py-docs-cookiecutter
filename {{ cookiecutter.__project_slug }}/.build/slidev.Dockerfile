# Slidev Dockerfile for {{ cookiecutter.project_name }}
# Base image with Node.js for running Slidev

FROM node:20-alpine

# Install system dependencies
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Set Chromium path for Playwright
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Set working directory
WORKDIR /slidev

# Install Slidev globally
RUN npm install -g @slidev/cli

# Expose port for Slidev dev server
EXPOSE 3030

# Default command (can be overridden)
CMD ["slidev", "--help"]

