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
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{password}@{host}:{port}/{db}{args}'.format(
        dialect=os.getenv('DB_DIALECT', 'mysql'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASS', 'password'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 3306),
        db=os.getenv('DB_NAME', 'gplogger'),
        args=os.getenv('DB_ARGUMENTS', '?charset=utf8mb4')
    )
