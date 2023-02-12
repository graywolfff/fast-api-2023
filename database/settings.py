from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = '.env'


setting = Settings()
