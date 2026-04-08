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
# Cloud Run Port
# ------------------------------------------------------------
EXPOSE 8080

# ------------------------------------------------------------
# Start BOTH FastAPI + Streamlit
# ------------------------------------------------------------
CMD bash -c "\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false"