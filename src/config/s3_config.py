import boto3
from botocore.config import Config
from config.config import settings


s3_config = Config(
    region_name=settings.S3_AWS_DEFAULT_REGION,
    signature_version=settings.S3_SIGNATURE_VERSION,
    retries={
        'max_attempts': settings.S3_AWS_MAX_ATTEMPTS,
        'mode': settings.S3_AWS_RETRY_MODE,
    }
)

s3_client = boto3.client("s3")

s3_resource = boto3.resource('s3')

