from pydantic import BaseSettings

# Class
class Settings(BaseSettings):
    api_key: str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name:str

    
    class Config:
        env_file = ".env"

# Instance 
settings = Settings()