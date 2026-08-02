import boto3
from pathlib import Path

# parent folder
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

# Connect to local MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='radhe',
    aws_secret_access_key='radhepassword123'
)

# Upload cleaned file
local_file = DATA_DIR / "ttc-bus-delay-data-2024-clean.xlsx"
bucket_name = "ttc-transit-data"
remote_filename = "ttc-bus-delay-data-2024-clean.xlsx"

s3.upload_file(str(local_file), bucket_name, remote_filename)

print(f"Uploaded {local_file.name} to bucket '{bucket_name}'")

# listing bucket contents (confirmation)
response = s3.list_objects_v2(Bucket=bucket_name)
print("\nFiles currently in bucket:")
for obj in response.get('Contents', []):
    print(f" - {obj['Key']} ({obj['Size']} bytes)")