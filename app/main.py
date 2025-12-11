
"""
Simple FastAPI application that talks to MinIO using boto3.

Each important line has a comment explaining what it does.
"""

import os
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import boto3
from botocore.client import Config

# Read MinIO configuration from environment variables.
# These will be supplied by Kubernetes ConfigMap.
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "demo-bucket")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

# Create a boto3 S3 client configured for MinIO (S3-compatible).
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,  # URL of MinIO server
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),  # S3 signature version
    region_name="us-east-1",  # Dummy region, MinIO does not enforce it
)

# Create FastAPI app instance.
app = FastAPI(title="MinIO Demo API", description="Upload & list files in MinIO via boto3")


@app.get("/")
def root():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "message": "MinIO demo API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a single file to the configured MinIO bucket.
    """
    try:
        # Read file contents into memory.
        contents = await file.read()

        # Use the original filename as the object key.
        object_key = file.filename

        # Upload the file to MinIO.
        s3_client.put_object(
            Bucket=MINIO_BUCKET,
            Key=object_key,
            Body=contents,
        )

        return {"status": "success", "bucket": MINIO_BUCKET, "key": object_key}
    except Exception as e:
        # The JSONResponse allows us to control status code & body.
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})


@app.get("/list")
def list_files() -> List[str]:
    """
    List all objects inside the MinIO bucket.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=MINIO_BUCKET)

        # If there are no contents, return an empty list.
        if "Contents" not in response:
            return []

        keys = [obj["Key"] for obj in response["Contents"]]
        return keys
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
