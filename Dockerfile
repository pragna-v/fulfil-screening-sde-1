# Use a small official Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory and set working dir
WORKDIR /code

# system deps (for psycopg2 and build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy dependency spec first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create upload temp dir
RUN mkdir -p /code/tmp

# Expose port for FastAPI app
EXPOSE 8000

# Default command (docker-compose overrides this for worker)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
