import time

from utils.util_logger import Logger

class ServiceManager:

    def __init__(self, logger: Logger, service_list=None):
        self.services = service_list or []
        self.logger = logger

    def add_service(self, service):
        self.services.append(service)
        self.logger.info(f"Added {service} to monitoring list.")

    def remove_service(self, service):
        self.services.remove(service)
        self.logger.info(f"Removed {service} from monitoring list.")

    def check_service_health(self, service_url):
        # 判斷 service 是否正常
        # if health:
        #   return True
        # else:
        #   return False
        time.sleep(1)  
        return True

    def start(self):
        while True:
            for service in self.services:
                if self.check_service_health(service):
                    self.logger.info(f"{service} is up and running.")
                else:
                    self.logger.error(f"{service} is down. Stopping its monitoring.")
                    self.remove_service(service)
            time.sleep(30)  # 每30秒檢查一次全部的services


    def stop(self):
        self.services = []
        self.logger.info("Stopped monitoring all services.")

    # If you need to restart the service manager, you can stop and then start again
    def restart(self):
        self.stop()
        self.start()