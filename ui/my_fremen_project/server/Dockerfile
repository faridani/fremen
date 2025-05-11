# Use Python 3.12 slim as the base
FROM python:3.12-slim

# Create the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Command to run
CMD ["python", "main.py"]
