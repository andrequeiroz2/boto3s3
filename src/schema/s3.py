from fastapi_utils.api_model import APIModel


class BucketLocationPostSchema(APIModel):
    path_name: str
    file_name: str


class BucketListSchema(APIModel):
    buckets: list = []


class BucketExistSchema(APIModel):
    is_exist: bool


class BucketIsSuccessSchema(APIModel):
    is_success: bool


class BucketImageNameSchema(APIModel):
    image_name: str
