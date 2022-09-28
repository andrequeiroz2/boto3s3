import pytest
from business.s3 import S3
from schema.s3 import BucketImageNameSchema

file = {'file': open("./test/locate_thanos.jpeg", "rb")}
user_guid = "test"
path_name_location = "location"
image_name_download = BucketImageNameSchema(image_name="locate_thanos.jpeg")


class Image(object):
    file = open("./test/locate_thanos.jpeg", "rb")
    filename = "locate_thanos.jpeg"


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


@pytest.mark.asyncio
async def test_is_exist_path():
    my_client = S3()
    result = await my_client.is_exist_path(user_guid)
    assert result.is_exist is True


@pytest.mark.asyncio
async def test_upload_image_location():
    my_client = S3()
    result = await my_client.upload_file(Image, user_guid, path_name_location)
    assert result.is_success is True


@pytest.mark.asyncio
async def test_download_image_location():
    my_client = S3()
    result = await my_client.download_image(user_guid, path_name_location, image_name_download)
    assert result.is_success is True
