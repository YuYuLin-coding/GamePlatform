from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from utils.util_logger import Logger
from utils.util_serviceManager import ServiceManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = Logger()
    app.state.service_manager = ServiceManager(logger = app.state.logger, service_list = Config.service_list)
    app.state.service_manager
    yield
    app.state.logger.info("Lifespan end: DB session closed")

app = FastAPI(lifespan=lifespan)
origins = [service["url"] for service in Config.service_list.values()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Logging server is starting"

@app.post("/reconnect/{service_name}")
async def reconnect_service(service_name: str):
    service_manager: ServiceManager = app.state.service_manager
    result = service_manager.reconnect(service_name)
    return result

from app.api import log_api

app.include_router(log_api.router)