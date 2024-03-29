import uvicorn
from logging import WARNING
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from presentation.api.middlewares.logger import RequestLogMiddleware
from chat.presentation.api.cfg import api_settings


from chat.presentation.api.controllers.user import router as users_router
from chat.presentation.api.auth.controller import router as auth_router


MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    ),
    # Middleware(ClientMiddleware),
    Middleware(RequestLogMiddleware),
]

app = FastAPI(
    title="ChatExample",
    version="1.0.0",
    middleware=MIDDLEWARES,
    debug=True

)

ROUTERS = [
    users_router,
    auth_router,

]

for router in ROUTERS:
    app.include_router(router)


def main():
    # TODO: use logger
    print("Server Start...")
    uvicorn.run(
                app="chat.presentation.api.main:app",
                host=api_settings.HOST,
                port=api_settings.PORT,
                reload=api_settings.RELOAD,
                workers=api_settings.WORKERS,
                log_level=WARNING,
                )


if __name__ == "__main__":
    main()

