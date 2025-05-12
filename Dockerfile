# Use the official Python image from Docker Hub as the base image
FROM python:3.11

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all the files from the current directory to the working directory inside the container
COPY . .

# Install Python dependencies from the requirements.txt file without caching for smaller image size
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Start the application using Gunicorn on port 8080, targeting the Flask app defined as "app:app"
CMD ["gunicorn", "-b", ":8080", "app:app"]
