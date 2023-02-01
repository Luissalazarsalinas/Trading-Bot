from pydantic import BaseSettings

# Class
class Settings(BaseSettings):
    api_key: str
    
    class Config:
        env_file = ".env"

# Instance 
settings = Settings()