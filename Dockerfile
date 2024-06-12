# Stage 1: Base image for both architectures
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Create an empty .env file (if needed)
RUN touch .env

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# Stage 2: Install Chromium and Chromedriver for amd64 architecture
FROM base AS amd64
RUN apt-get update && \
    apt-get install -y wget gnupg unzip --no-install-recommends && \
    apt-get install -y chromium chromium-driver && \
    apt-get purge -y --auto-remove wget gnupg && \
    rm -rf /var/lib/apt/lists/*

# Stage 3: Install Chromium and Chromedriver for arm64 architecture
FROM base AS arm64
RUN apt-get update && \
    apt-get install -y wget gnupg unzip --no-install-recommends && \
    apt-get install -y chromium chromium-driver && \
    apt-get purge -y --auto-remove wget gnupg && \
    rm -rf /var/lib/apt/lists/*

# Stage 4: Final stage to combine and copy the application code
FROM base AS final

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]
