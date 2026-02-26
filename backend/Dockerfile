# Multi-stage build for Python Flask API
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create directory for database
RUN mkdir -p /app/data

# Expose port
EXPOSE 5001

# Set environment variables
ENV FLASK_APP=compliance_discovery.api_server
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/data/sessions.db

# Run the application
CMD ["python", "-m", "compliance_discovery.api_server"]
