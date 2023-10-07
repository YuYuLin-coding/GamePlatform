import os

class Config(object):
    VERSION_PREFIX='v1.0'
    VERSION = '2310'
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{password}@{host}:{port}/{db}{args}'.format(
        dialect=os.getenv('DB_DIALECT', 'mysql'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASS', 'password'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 3306),
        db=os.getenv('DB_NAME', 'gpuser'),
        args=os.getenv('DB_ARGUMENTS', '?charset=utf8mb4')
    )
    SECRET_PEPPER = "ChangeYourOwnKeyHere"