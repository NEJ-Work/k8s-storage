from fastapi import FastAPI, UploadFile, File, HTTPException
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os

app = FastAPI()

# Initialize S3 client (uses environment variables or IAM role)
s3 = boto3.client("s3")

BUCKET_NAME = os.getenv("S3_BUCKET","generic-bucket")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read file content into memory
        file_bytes = await file.read()

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file.filename,
            Body=file_bytes,
            ContentType=file.content_type
        )

        return {"status": "success", "filename": file.filename}

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))