import asyncio

import httpx

from utils.util_logger import Logger

class ServiceManager:
    def __init__(self, logger: Logger, service_list=None):
        self.services = service_list or {}
        self.logger = logger

    def add_service(self, service_name, service_url):
        self.services[service_name] = {
            "url": service_url,
            "status": "up",
            "last_checked": None,
            "retry_count": 0
        }
        self.logger.info(f"Added {service_name} at {service_url} to monitoring list.")
    
    def reconnect(self, service_name: str) -> dict:
        if service_name in self.services:
            self.services[service_name]["retry_count"] = 0
            self.services[service_name]["status"] = "up"
            return {"status": "Service reconnected"}
        else:
            return {"error": "Service not found"}
        
    def remove_service(self, service_name):
        del self.services[service_name]
        self.logger.info(f"Removed {service_name} from monitoring list.")

    async def check_service_health(self, service_name, service_url):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(service_url)
                return resp.status_code == 200
        except Exception as e:
            self.logger.error(f"Error checking {service_name}: {e}")
            return False

    async def start(self):
        while True:
            for service_name, service_data in list(self.services.items()):
                healthy = await self.check_service_health(service_name, service_data["url"])
                if healthy:
                    self.logger.info(f"{service_name} is up and running.")
                else:
                    service_data["retry_count"] += 1
                    if service_data["retry_count"] >= 3:
                        self.logger.error(f"{service_name} is down. Stopping its monitoring.")
                        self.remove_service(service_name)
            await asyncio.sleep(30)  # 每30秒檢查一次全部的services

    async def stop(self):
        self.services = {}
        self.logger.info("Stopped monitoring all services.")