# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy app code
COPY app-simple.py .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app-simple.py"]
