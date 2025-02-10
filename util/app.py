import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from container.constructor import Constructor as ContainerConstructor
from controller.constructor import Constructor as RouterConstructor
from util.custom_logging import api_logger
from core.config import config
class AppRunner:
    def __init__(self):
        self.config = config
        self.app: FastAPI = FastAPI()

        ContainerConstructor()
        for router_name, router_object in RouterConstructor().__dict__.items():
            self.app.include_router(router_object)


        self.app.mount('/static', StaticFiles(directory="static"), name="static")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 모든 도메인 허용 (배포 환경에서는 특정 도메인만 허용)
            allow_credentials=True,
            allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
            allow_headers=["*"],  # 모든 헤더 허용
        )

        @self.app.middleware("http")
        async def log_requests(request: Request, call_next) -> Request:
            # 요청 로깅
            api_logger.info(f"Request {request.method} {request.url}")
            response = await call_next(request)
            # 응답 로깅
            api_logger.info(f"Response status code: {response.status_code}")
            return response

    def run(self):
        uvicorn.run(self.app, port=self.config.port, host=self.config.host)
