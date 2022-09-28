import os
from config.s3_config import s3_client
from schema.s3 import BucketListSchema, BucketExistSchema, BucketUploadSchema, BucketImageNameSchema
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
    async def upload_file(image, user_guid: str, path_name: str) -> BucketUploadSchema:
        try:
            s3_client.upload_fileobj(
                image.file,
                settings.S3_AWS_BUCKET_NAME,
                f"{user_guid}/{path_name}/{image.filename}")
        except ClientError:
            return BucketUploadSchema(is_success=False)
        return BucketUploadSchema(is_success=True)

    async def get_image(self, user_guid: str, path: str, image_name: BucketImageNameSchema):

        client_path = f"./s3_downloads/{user_guid}/{path}"

        if not self._isdir(client_path):
            os.makedirs(client_path)

        s3_client.download_file(
            settings.S3_AWS_BUCKET_NAME,
            f"{user_guid}/{path}/{image_name.image_name}",
            f"./s3_downloads/{user_guid}/{path}/{image_name.image_name}"

        )




        # s3_client.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
        return ""

    @staticmethod
    def _isdir(path: str):
        return os.path.isdir(path)
