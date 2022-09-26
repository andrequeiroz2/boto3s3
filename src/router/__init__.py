from starlette.responses import RedirectResponse

from router.router import api_router


def routers_init(app):
    @app.get("/", include_in_schema=False)  # skipcq: PTC-W0065
    def docs():  # skipcq: PTC-W0065
        return RedirectResponse(url="/docs/")

    app.include_router(api_router, prefix="/api")
