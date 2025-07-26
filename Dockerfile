FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for numpy, pandas, etc.
RUN apt-get update && \
    apt-get install -y build-essential libzbar0 libglib2.0-0 libsm6 libxext6 libxrender-dev python3-dev g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

COPY phishguard/ .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["python", "start_app.py"]