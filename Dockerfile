# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Remove Windows-specific dependencies and editable install
RUN sed -i '/wincertstore/d' requirements.txt && \
    sed -i '/-e \./d' requirements.txt

# Create venv and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3.9-slim as runner

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Expose the application port
EXPOSE 8080

# Environment variables
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8080

CMD ["python", "app.py"]
