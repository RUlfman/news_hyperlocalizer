# Use the official Python image as a base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment
RUN . venv/bin/activate

# Install dependencies within the virtual environment
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
