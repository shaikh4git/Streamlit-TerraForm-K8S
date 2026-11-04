FROM python:3.12-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies during image build along with the Cache downloaded Python packages both Docker layer and pip cache to speed up future builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m venv /opt/ansible && \
    /opt/ansible/bin/python -m pip install ansible requests docker
# Copy Streamlit application!!!!
COPY app.py .

# Create a non-root user and set ownership!!
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

# Run the application as non-root
USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]