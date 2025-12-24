# ------------------------------------------------------------
# Base Image
# ------------------------------------------------------------
FROM python:3.10-slim

# ------------------------------------------------------------
# Environment Configuration
# ------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ------------------------------------------------------------
# Application Directory
# ------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------
# System Dependencies
# ------------------------------------------------------------
# poppler-utils  → PDF text extraction
# build-essential → native Python package builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Python Dependencies
# ------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------
# Application Source
# ------------------------------------------------------------
COPY . .

# ------------------------------------------------------------
# Network Configuration (Cloud Run Standard)
# ------------------------------------------------------------
EXPOSE 8080

# ------------------------------------------------------------
# Application Entrypoint
# ------------------------------------------------------------
CMD ["streamlit", "run", "app.py", \
     "--server.port=$PORT", \
     "--server.address=0.0.0.0", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]

