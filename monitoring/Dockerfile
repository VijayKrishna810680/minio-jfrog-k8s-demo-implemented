# Use official Python image
FROM python:3.11-slim
WORKDIR /monitoring
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn
EXPOSE 9090
CMD ["uvicorn", "monitoring_api:router", "--host", "0.0.0.0", "--port", "9090"]
