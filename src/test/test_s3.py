import pytest
from tempfile import NamedTemporaryFile

from business.s3 import S3


@pytest.fixture
def bucket_name():
    return "my-test-bucket"


@pytest.fixture
def s3_test(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    yield


@pytest.mark.asyncio
async def test_list_buckets(s3_client, s3_test):
    my_client = S3()
    buckets = await my_client.get_all()
    for x in buckets.buckets:
        if x.get("Name") == "andrelinuxtips":
            assert x.get("Name") == "andrelinuxtips"