from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from utils.util_logger import Logger
from utils.util_serviceManager import ServiceManager

logger = Logger()
app = FastAPI()
service_manager = ServiceManager(logger)

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

@app.post("/add_log")
async def add_log():
    return "Add log successfully"