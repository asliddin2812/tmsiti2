from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    UPLOAD_DIR: str
    MAX_FILE_SIZE: int

    class Config:
        env_file = ".env"

settings = Settings()
