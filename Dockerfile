# First stage: amd64 architecture
FROM --platform=linux/amd64 python:3 as amd64

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Create an empty .env file (if needed)
RUN touch .env

# Install Chrome and Chromedriver for amd64 architecture
RUN apt-get update && apt-get install -y wget gnupg unzip
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
&& unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip \
&& mv chromedriver /usr/local/bin/chromedriver \
&& chmod +x /usr/local/bin/chromedriver

# Second stage: arm64 architecture
FROM --platform=linux/arm64 python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Create an empty .env file (if needed)
RUN touch .env

# Install Chrome and Chromedriver for arm64 architecture
RUN apt-get update && apt-get install -y wget gnupg unzip
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=arm64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
&& unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip \
&& mv chromedriver /usr/local/bin/chromedriver \
&& chmod +x /usr/local/bin/chromedriver

# Copy the current directory contents into the container at /app
COPY . /app

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]