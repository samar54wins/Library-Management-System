# Use Python 3.11 as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unixodbc-dev \
    libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY .env /app/

# Copy the entire project code into the container
COPY . /app/
# Expose the port for the application
EXPOSE 8000
EXPOSE 80

# Command to run the application using run.py
CMD ["python", "run.py"]
