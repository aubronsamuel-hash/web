from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .auth import router as auth_router
from .logging_setup import configure_logging, get_logger
from .middleware import RequestIdMiddleware, get_request_id
from .settings import get_settings

configure_logging()
log = get_logger("app")


def create_app() -> FastAPI:
    app = FastAPI(title=get_settings().app_name)
    app.add_middleware(RequestIdMiddleware)

    @app.get("/healthz")
    async def healthz(request: Request):
        rid = get_request_id()
        log.info("Healthz OK", extra={"path": str(request.url.path)})
        return JSONResponse({"status": "ok"}, headers={get_settings().request_id_header: rid})

    app.include_router(auth_router)

    return app


app = create_app()
