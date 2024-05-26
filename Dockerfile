# Use a multi-architecture base image
FROM --platform=$TARGETPLATFORM python:3

# Set build arguments
ARG TARGETPLATFORM

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Create an empty .env file (if needed)
RUN touch .env

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# Install Chrome and Chromedriver for both architectures
RUN apt-get update && apt-get install -y wget gnupg unzip && \
    case "$TARGETPLATFORM" in \
    "linux/amd64") \
        wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
        apt-get update && apt-get install -y google-chrome-stable \
        ;; \
    "linux/arm64") \
        wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        apt-get update && apt-get install -y libxss1 libappindicator1 libindicator7 && \
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_arm64.deb && \
        dpkg -i google-chrome-stable_current_arm64.deb || apt-get -fy install && \
        rm google-chrome-stable_current_arm64.deb \
        ;; \
    esac

# Install Chromedriver
RUN wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]
