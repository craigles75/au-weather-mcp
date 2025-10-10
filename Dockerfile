# Australian Weather MCP Server Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY server.py .
COPY weather.py .

# Install dependencies
RUN pip install --no-cache-dir -e .

# The server runs on stdio, so no ports to expose
# Command will be run via docker run with stdio
ENTRYPOINT ["python", "server.py"]
