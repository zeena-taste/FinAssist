# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file securely into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the correct cloud run port
ENV PORT=8080
EXPOSE $PORT

# Command to run the FastApi application properly bound to the explicit host
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
