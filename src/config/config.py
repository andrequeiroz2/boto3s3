import os
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, root_validator
from functools import lru_cache

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    API_TITLE = os.getenv("API_TITLE")
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    DEBUG: bool = os.getenv("DEBUG")
    S3_AWS_DEFAULT_REGION = os.getenv("S3_AWS_DEFAULT_REGION")
    S3_SIGNATURE_VERSION = os.getenv("S3_SIGNATURE_VERSION")
    S3_AWS_MAX_ATTEMPTS: int = int(os.getenv("S3_AWS_MAX_ATTEMPTS"))
    S3_AWS_RETRY_MODE = os.getenv("S3_AWS_RETRY_MODE")
    S3_AWS_ACCESS_KEY_ID = os.getenv("S3_AWS_ACCESS_KEY_ID")
    S3_AWS_SECRET_ACCESS_KEY = os.getenv("S3_AWS_SECRET_ACCESS_KEY")
    S3_AWS_BUCKET_NAME = os.getenv("S3_AWS_BUCKET_NAME")

    @root_validator(pre=False)
    def validate_all(cls, values):  # skipcq: PYL-R0201
        for key, value in values.items():
            if any(
                    (
                            value is None,
                            isinstance(value, str) and not value,
                            isinstance(value, str) and value.isspace(),
                    )
            ):
                raise ValueError(f"Error in file (.env), check variable {key}")
        return values

@lru_cache
def get_api_settings() -> Settings:
    """
    Faz cache das configuracoes
    :return: Configuracoes armazenadas no cache
    """
    return Settings()


settings = get_api_settings()
