from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from business.s3 import S3
from schema.s3 import BucketListSchema, BucketExistSchema, BucketUploadSchema, BucketImageNameSchema
from fastapi import UploadFile, Depends

s3_router = InferringRouter()


@cbv(s3_router)
class S3Router:

    @s3_router.get("/all/")
    async def get_all(self) -> BucketListSchema:
        return await S3().get_all()

    @s3_router.get("/exist/{user_guid}/")
    async def get_exist(self, user_guid: str) -> BucketExistSchema:
        return await S3().is_exist_path(user_guid)

    @s3_router.post("/{user_guid}/")
    async def post_bucket(self, image: UploadFile, path_name: str, user_guid: str) -> BucketUploadSchema:
        return await S3().upload_file(image, user_guid, path_name)

    @s3_router.get("/image/{user_guid}/{path}")
    async def get_image(self, user_guid: str, path: str, image_name: BucketImageNameSchema):
        return await S3().get_image(user_guid, path, image_name)
