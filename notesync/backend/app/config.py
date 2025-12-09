from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://mongo:27017"
    MONGO_DB: str = "notesync"
    SECRET_KEY: str = "change-me-to-a-secure-random-string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
