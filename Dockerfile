# Set build arguments
ARG TARGETPLATFORM=linux/amd64

# Use a multi-architecture base image
FROM --platform=$TARGETPLATFORM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CHROMEDRIVER_VERSION=114.0.5735.90
ENV PATH="/usr/local/bin:$PATH"

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

# Install common dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip

# Install Chrome and Chromedriver for amd64 architecture
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
        wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
        apt-get update && apt-get install -y google-chrome-stable && \
        wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
        unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip && \
        mv chromedriver /usr/local/bin/chromedriver && \
        chmod +x /usr/local/bin/chromedriver; \
    fi

# Install Chrome and Chromedriver for arm64 architecture
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
        echo "Starting Chrome installation for arm64"; \
        wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        apt-get update && apt-get install -y libxss1 libappindicator1 libindicator7 && \
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_arm64.deb && \
        dpkg -i google-chrome-stable_current_arm64.deb && \
        if [ $? -ne 0 ]; then \
            echo "First dpkg install failed, running apt-get -fy install"; \
            apt-get -fy install && dpkg -i google-chrome-stable_current_arm64.deb; \
        fi && \
        rm google-chrome-stable_current_arm64.deb && \
        wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
        unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip && \
        mv chromedriver /usr/local/bin/chromedriver && \
        chmod +x /usr/local/bin/chromedriver; \
    fi

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]
