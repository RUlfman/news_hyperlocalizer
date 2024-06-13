# Stage 1: Base image for both architectures
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

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

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set up chromedriver executable path
ENV PATH="/usr/lib/chromium:${PATH}"

# Confirm installation
RUN chromium --version && chromedriver --version

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]
