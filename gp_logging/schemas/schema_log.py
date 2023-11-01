from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class LogLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"
    CRITICAL = "critical"

class ServiceName(Enum):
    USER_SERVICE = "user_service"
    CLIENT_SERVICE = "client_service"
    GAME_SERVICE = "game_service"

class BaseLog(BaseModel):
    id: Optional[int] = Field(None, description="自動增長的主鍵ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="日誌創建的時間")
    service_name: ServiceName = Field(..., description="發送此日誌的服務名稱")
    level: LogLevel = Field(..., description="日誌的級別")
    message: str = Field(..., description="日誌的主要信息")
    traceback: Optional[str] = Field(None, description="錯誤追踪資訊（如果有）")
    metadata: Optional[dict] = Field({}, description="其他相關的元數據")
    hostname: Optional[str] = Field(None, description="主機名稱")

class UserLog(BaseLog):
    user_id: int = Field(..., description="與特定用戶相關的ID")
    action: Optional[str] = Field(None, description="用戶動作，如'login', 'logout'等")
    api_endpoint: Optional[str] = Field(None, description="被調用的API端點")

class ClientLog(UserLog):  # UserLog already has user_id, action, and api_endpoint
    client_type: str = Field(..., description="客戶端類型，如'web', 'mobile', 'desktop'等")

class GameLog(UserLog):  # UserLog already has user_id, action, and api_endpoint
    game_name: str = Field(..., description="遊戲名稱")
    game_action: str = Field(..., description="遊戲動作，如'start', 'pause', 'end'等")
