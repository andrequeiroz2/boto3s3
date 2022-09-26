from typing import Optional

from fastapi_utils.api_model import APIModel


class ExceptionSchema(APIModel):
    msg: Optional[str]
    detail: Optional[str]