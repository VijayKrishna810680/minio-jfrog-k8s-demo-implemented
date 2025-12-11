import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1"
)

resp = s3.list_buckets()
print("Buckets:")
for b in resp.get("Buckets", []):
    print(" -", b["Name"])
