from fastapi_utils.inferring_router import InferringRouter
from dependencie.serializer import ORJSONResponse
from endpoint.s3 import s3_router
from schema.exception import ExceptionSchema

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

api_router = InferringRouter(
    default_response_class=ORJSONResponse,
    responses={
        HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        HTTP_422_UNPROCESSABLE_ENTITY: {"model": ExceptionSchema},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
)

api_router.include_router(s3_router, prefix="/bucket", tags=["Bucket"])
