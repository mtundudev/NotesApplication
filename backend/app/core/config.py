from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    EXPIRE_ACCESS_TOKEN:int
    APP_NAME:str
    ALGORITHM:str
    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
settings=Settings()    
    
    
    