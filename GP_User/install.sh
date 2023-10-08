# 初始化alembic版本
pipenv run alembic init alembic

#在alembic/env.py檔案更改如下
from db.database import Base
import db.models
target_metadata = Base.metadata

# 在alembic.ini 中的url參數改為如下，其中[]內設定改為自己環境
sqlalchemy.url = mysql+mysqlconnector://[username]:[password]@[host]/[database_name]

#生成mirations file
pipenv run alembic revision --autogenerate -m "first migrate for user table"

# 執行upgrade
pipenv run alembic upgrade head 