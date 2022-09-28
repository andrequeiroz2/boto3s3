import os
from config.s3_config import s3_client
from schema.s3 import BucketListSchema, BucketExistSchema, BucketIsSuccessSchema, BucketImageNameSchema
from config.config import settings
from botocore.errorfactory import ClientError


class S3:

    base_path_download = "./s3_downloads/"

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
    async def upload_file(image, user_guid: str, path_name: str) -> BucketIsSuccessSchema:
        try:
            s3_client.upload_fileobj(
                image.file,
                settings.S3_AWS_BUCKET_NAME,
                f"{user_guid}/{path_name}/{image.filename}")
        except ClientError:
            return BucketIsSuccessSchema(is_success=False)
        return BucketIsSuccessSchema(is_success=True)

    async def download_image(
            self,
            user_guid: str,
            path: str, image_name: BucketImageNameSchema) -> BucketIsSuccessSchema:

        if not self._isdir(self.base_path_download, user_guid, path):
            self._create_directory(self.base_path_download, user_guid, path)

        try:
            s3_client.download_file(
                settings.S3_AWS_BUCKET_NAME,
                f"{user_guid}/{path}/{image_name.image_name}",
                f"{self.base_path_download}/{user_guid}/{path}/{image_name.image_name}"

            )
        except ClientError as err:
            raise err

        return BucketIsSuccessSchema(is_success=True)

    @staticmethod
    def _isdir(base_path_download: str, user_guid: str, path: str) -> bool:
        client_path = f"{base_path_download}/{user_guid}/{path}"
        try:
            result = os.path.isdir(client_path)
        except OSError as error:
            raise error
        return result

    @staticmethod
    def _create_directory(base_path_download: str, user_guid: str, path: str):
        client_path = f"{base_path_download}/{user_guid}/{path}"
        try:
            os.makedirs(client_path)
        except OSError as error:
            raise error
