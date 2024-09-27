# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy .env file if it' used by Django settings
COPY .env .env

# Run Django using Gunicorn
CMD ["gunicorn", "auditions.wsgi:application", "--bind", "0.0.0.0:8000"]
