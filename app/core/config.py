from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = 'Помощь котикам'
    database_url: str = 'sqlite+aiosqlite:///:memory:'
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    life_token = '2400'
    min_password_length = 5

    class Config:
        env_file = '.env'


settings = Settings()
