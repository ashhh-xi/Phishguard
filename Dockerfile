# Use official Python 3.10 image
FROM python:3.10-slim

# Set work directory
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Install system dependencies (if needed)


# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port (Flask default is 5000, Gunicorn default is 8000)
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "--chdir", "phishguard", "app:app", "--bind", "0.0.0.0:${PORT:-8000}"] 
