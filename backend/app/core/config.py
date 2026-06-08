from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 所有字段都没有默认值，强制从环境变量或 .env 文件读取
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: List[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# 实例化时如果缺少变量会抛出 ValidationError
settings = Settings()