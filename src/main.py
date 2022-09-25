import uvicorn
from fastapi import FastAPI
from config.config import settings
from config.s3_config import s3_client
# import dependencie
from router import routers_init


def create_app() -> FastAPI:

    fastapi_app = FastAPI(title=settings.API_TITLE, debug=settings.DEBUG)
    routers_init(fastapi_app)
    return fastapi_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL)
