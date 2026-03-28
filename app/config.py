from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinAassist"
    DATABASE_URL: str = "sqlite:///./finaassist.db"
    GEMINI_API_KEY: str = "" # Set this in environment variable or .env file

    class Config:
        env_file = ".env"

settings = Settings()
