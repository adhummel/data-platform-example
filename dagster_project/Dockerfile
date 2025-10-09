# Multi-stage build for optimal image size
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Set Python path so dagster can find the module
ENV PYTHONPATH=/app:$PYTHONPATH

# Expose Dagster webserver port
EXPOSE 3000

# Default command runs webserver, but can be overridden for daemon
CMD ["dagster", "dev", "-m", "dagster_project", "-h", "0.0.0.0", "-p", "3000"]
