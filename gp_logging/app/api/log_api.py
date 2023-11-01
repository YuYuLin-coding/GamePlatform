from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_client_ip
from app.main import app
from db.database import get_db
from schemas import schema_log

router = APIRouter(
    prefix='/api/log',
    tags=['api_log']
)

router = APIRouter()

@router.post("/add/user_service", response_model=schema_log.UserLog)
async def add_user_log(data: schema_log.UserLog, client_ip: str = Depends(get_client_ip)):
    if check_service_ip(schema_log.ServiceName.USER_SERVICE, client_ip, app):
        # ... 處理data
        return data
    else:
        raise HTTPException(status_code=403, detail="IP mismatch")

@router.post("/add/client_service", response_model=schema_log.ClientLog)
async def add_client_log(data: schema_log.ClientLog, client_ip: str = Depends(get_client_ip)):
    if check_service_ip(schema_log.ServiceName.CLIENT_SERVICE, client_ip, app):
        # ... 處理data
        return data
    else:
        raise HTTPException(status_code=403, detail="IP mismatch")

@router.post("/add/game_service", response_model=schema_log.GameLog)
async def add_game_log(data: schema_log.GameLog, client_ip: str = Depends(get_client_ip)):
    if check_service_ip(schema_log.ServiceName.GAME_SERVICE, client_ip, app):
        # ... 處理data
        return data
    else:
        raise HTTPException(status_code=403, detail="IP mismatch")

def check_service_ip(service_name: schema_log.ServiceName, client_ip: str) -> bool:
    service_url = app.state.service_manager.services.get(service_name.value, {}).get("url")
    if service_url:
        expected_ip = service_url.split("://")[1].split("/")[0]  # 取得url中的ip部分
        return expected_ip == client_ip
    return False