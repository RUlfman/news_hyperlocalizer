# Use the official Python image as a base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies within the virtual environment
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Add a label to link the image to the GitHub repository
LABEL org.opencontainers.image.source=https://github.com/RUlfman/news_hyperlocalizer

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["bash", "./entrypoint.sh"]