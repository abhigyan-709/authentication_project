# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY app/requirements.txt . 

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory to the container
COPY app/ . 

# Expose the port that the FastAPI application runs on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
