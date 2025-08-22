from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .auth import router as auth_router
from .db import get_engine
from .logging_setup import configure_logging, get_logger
from .middleware import RequestIdMiddleware, get_request_id
from .routers_availabilities import router as av_router  # type: ignore[import-untyped]
from .routers_intermittents import router as inter_router  # type: ignore[import-untyped]
from .routers_missions import router as missions_router  # type: ignore[import-untyped]
from .routers_planning import router as planning_router  # type: ignore[import-untyped]
from .routers_users import router as users_router
from .settings import get_settings

configure_logging()
log = get_logger("app")
get_engine()  # init engine early


def create_app() -> FastAPI:
    app = FastAPI(title=get_settings().app_name)
    app.add_middleware(RequestIdMiddleware)

    @app.get("/healthz")
    async def healthz(request: Request):
        rid = get_request_id()
        log.info("Healthz OK", extra={"path": str(request.url.path)})
        return JSONResponse(
            {"status": "ok"},
            headers={get_settings().request_id_header: rid},
        )

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(inter_router)
    app.include_router(missions_router)
    app.include_router(av_router)
    app.include_router(planning_router)

    return app


app = create_app()
