from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, Field

class ServiceStatus(Enum):
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class AuthMethod(Enum):
    BASIC = "basic"
    BEARER = "bearer"
    OAUTH2 = "oauth2"
    NONE = "none"

class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    PARTIAL = "partial"

class ServiceInfo(BaseModel):
    service_name: str = Field(..., description="服務名稱")
    service_version: str = Field(..., description="服務版本")
    service_description: Optional[str] = Field(None, description="服務描述")
    service_url: HttpUrl = Field(..., description="服務的URL地址")

class OperationalInfo(BaseModel):
    service_status: ServiceStatus = Field(..., description="服務狀態")
    service_started_at: datetime = Field(default_factory=datetime.utcnow, description="服務開始時間")
    service_updated_at: datetime = Field(default_factory=datetime.utcnow, description="服務最後更新時間")
    service_endpoints: Optional[List[HttpUrl]] = Field(None, description="服務的所有端點")

class ResourceUsage(BaseModel):
    cpu_usage: float = Field(..., description="CPU使用率")
    memory_usage: float = Field(..., description="內存使用率")
    storage_usage: float = Field(..., description="存儲使用率")

class SecurityInfo(BaseModel):
    auth_required: bool = Field(..., description="是否需要驗證")
    auth_method: Optional[AuthMethod] = Field(None, description="驗證方法")

class HealthMonitoring(BaseModel):
    health_endpoint: HttpUrl = Field(..., description="健康監控端點")
    last_health_check: datetime = Field(default_factory=datetime.utcnow, description="最後一次健康檢查時間")
    health_status: HealthStatus = Field(..., description="健康狀態")

# Combining all into a Service Model
class Service(BaseModel):
    service_info: ServiceInfo = Field(..., description="服務基本資訊")
    operational_info: OperationalInfo = Field(..., description="運營資訊")
    resource_usage: ResourceUsage = Field(..., description="資源使用情況")
    security_info: SecurityInfo = Field(..., description="安全相關資訊")
    health_monitoring: HealthMonitoring = Field(..., description="健康監控資訊")
