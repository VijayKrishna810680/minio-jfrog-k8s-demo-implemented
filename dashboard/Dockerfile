FROM python:3.11-slim

WORKDIR /dashboard

COPY dashboard/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard app files (from project root context)
COPY dashboard/ ./

# Copy shared modules from project root
COPY core/ ./core
COPY ai/ ./ai

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
