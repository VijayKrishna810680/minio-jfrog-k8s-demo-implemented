FROM python:3.11-slim
WORKDIR /ai
COPY ai/requirements.txt /ai/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true
COPY ai/ /ai
EXPOSE 5000
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "5000"]
