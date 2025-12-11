from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import boto3
from botocore.client import Config
from typing import List

# Read MinIO configuration from environment variables.
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "demo-bucket")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

router = APIRouter()

@router.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "MinIO demo API is running"}

@router.post("/upload", tags=["files"])
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        object_key = file.filename
        s3_client.put_object(
            Bucket=MINIO_BUCKET,
            Key=object_key,
            Body=contents,
        )
        return {"status": "success", "bucket": MINIO_BUCKET, "key": object_key}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

@router.get("/list", tags=["files"])
def list_files() -> List[str]:
    try:
        response = s3_client.list_objects_v2(Bucket=MINIO_BUCKET)
        if "Contents" not in response:
            return []
        keys = [obj["Key"] for obj in response["Contents"]]
        return keys
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
