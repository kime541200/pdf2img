FROM python:3.11-slim

# Install system dependencies (poppler-utils)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies and the package itself
RUN pip install --no-cache-dir ".[all]"

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "pdf2img.server:app", "--host", "0.0.0.0", "--port", "8000"]

