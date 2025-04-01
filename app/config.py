from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    BASE_URL: str = Field(default="http://localhost:8000")

    class Config:
        env_file = ".env"

settings = Settings() 