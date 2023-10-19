import os

class Config(object):
    RUN_MODE = os.environ.get('RUN_MODE', 'product')  # 如果沒有設定RUN_MODE，則默認為'product'
    service_list = {
        "service1": {
            "url": "http://127.0.0.1:8000",
            "status": "up",
            "last_checked": None,
            "retry_count": 0
        },
        "service2": {
            "url":  "http://127.0.0.1:5000",
            "status": "up",
            "last_checked": None,
            "retry_count": 0
        }
    }
