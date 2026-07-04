# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set PYTHONPATH so that imports from src work correctly
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Run main.py when the container launches. 
# main.py will exit with 0 if successful, or non-zero if there's an unhandled exception.
CMD ["python", "main.py"]
