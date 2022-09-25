from config.s3_config import s3_client, s3_resource
from schema.s3 import BucketListSchema, BucketExistSchema, BucketLocationPostSchema
from config.config import settings
from botocore.errorfactory import ClientError


class S3:
    @staticmethod
    async def get_all() -> BucketListSchema:
        buckets_list = []
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            buckets_list.append(bucket)
        return BucketListSchema(buckets=buckets_list)

    @staticmethod
    async def is_exist_path(user_guid: str) -> BucketExistSchema:
        try:
            s3_client.head_object(Bucket=settings.S3_AWS_BUCKET_NAME, Key=f"{user_guid}/")
        except ClientError as err:
            if err.response['Error']['Code'] == '404':
                return BucketExistSchema(is_exist=False)
            raise err
        return BucketExistSchema(is_exist=True)

    @staticmethod
    async def get_content(self, user_guid: str):
        bucket = s3_resource.Bucket(settings.S3_AWS_BUCKET_NAME)
        objs = bucket.objects.filter(Prefix=user_guid)
        oi = objs
        return "200"

    @staticmethod
    async def uploadfile(image, user_guid: str, path_name: str):
        try:
            s3_client.upload_fileobj(
                image.file,
                settings.S3_AWS_BUCKET_NAME,
                f"{user_guid}/{path_name}/{image.filename}")
        except ClientError as err:
            return False
        return True