# First stage: amd64 architecture
FROM --platform=linux/amd64 python:3 as amd64

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .
# Install dependencies within the virtual environment
RUN pip install -r requirements.txt

# Create an empty .env file
RUN touch .env

# Copy the current directory contents into the container at /app
COPY . /app

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# please review all the latest versions here:
# https://sites.google.com/a/chromium.org/chromedriver/
ENV CHROMEDRIVER_VERSION=114.0.5735.90

### install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

### install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
  && unzip chromedriver_linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

# Second stage: arm64 architecture
FROM --platform=linux/arm64 python:3

# Copy the necessary files from the amd64 stage
COPY --from=amd64 /usr/bin/google-chrome /usr/bin/
COPY --from=amd64 /opt/google/chrome /opt/google/chrome
COPY --from=amd64 /usr/bin/chromedriver /usr/bin/

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]