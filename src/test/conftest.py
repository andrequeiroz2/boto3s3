import boto3
import os
import pytest

from moto import mock_s3


os.environ["HOST"] = "127.0.0.1"
os.environ["PORT"] = "6000"
os.environ["LOG_LEVEL"] = "debug"
os.environ["DEBUG"] = "True"
os.environ["S3_AWS_MAX_ATTEMPTS"] = "5"
os.environ["S3_AWS_RETRY_MODE"] = "standard"
os.environ["S3_AWS_BUCKET_NAME"] = "andrelinuxtips"


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn
