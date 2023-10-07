from passlib.context import CryptContext
from config import Config  # 從config.py導入配置值

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_PEPPER = Config.SECRET_PEPPER

class Hash():
    def hash_password(password: str) -> str:
        return pwd_cxt.hash(password + SECRET_PEPPER)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_cxt.verify(plain_password + SECRET_PEPPER, hashed_password)