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

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# Please review all the latest versions here:
# https://sites.google.com/a/chromium.org/chromedriver/
ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y wget zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&& dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
&& rm google-chrome-stable_current_amd64.deb
RUN wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
&& unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip \
&& mv chromedriver /usr/local/bin/chromedriver \
&& chmod +x /usr/local/bin/chromedriver

# Second stage: arm64 architecture
FROM --platform=linux/arm64 python:3

# Copy the necessary files from the amd64 stage
COPY --from=amd64 /usr/local/bin/chromedriver /usr/local/bin/chromedriver
COPY --from=amd64 /usr/bin/google-chrome /usr/bin/google-chrome
COPY --from=amd64 /opt/google/chrome /opt/google/chrome

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
 
# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]