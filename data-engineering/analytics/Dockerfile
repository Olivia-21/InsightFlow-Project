# ─────────────────────────────────────────────────────────────────────────────
# InsightFlow — Streamlit Dashboard
# Data Engineer B: Carl Nyameakyere Crankson
#
# Build:   docker build -t insightflow-dashboard .
# Run:     docker run -p 8501:8501 insightflow-dashboard
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard source
COPY dashboard/ ./dashboard/
COPY data/       ./data/

# Streamlit config — disable telemetry and set default port
RUN mkdir -p ~/.streamlit && cat > ~/.streamlit/config.toml <<EOF
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#F47920"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F4F8"
textColor = "#1F4E79"
font = "sans serif"
EOF

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the dashboard
CMD ["streamlit", "run", "dashboard/reporting_dashboard.py", "--server.address=0.0.0.0"]
