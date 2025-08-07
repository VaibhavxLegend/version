# app/config/settings.py
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    app_name: str = "LLM Query System"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database (Optional - for hackathon can use simple file storage)
    db_user: str = Field("user", env="POSTGRES_USER")
    db_password: SecretStr = Field("password", env="POSTGRES_PASSWORD")
    db_host: str = Field("localhost", env="POSTGRES_HOST")
    db_port: int = Field(5432, env="POSTGRES_PORT")
    db_name: str = Field("llm_db", env="POSTGRES_DB")

    # API Keys
    pinecone_api_key: SecretStr = Field("dummy-key", env="PINECONE_API_KEY")
    pinecone_env: str = Field("us-east-1", env="PINECONE_ENVIRONMENT")
    gemini_api_key: SecretStr = Field("dummy-key", env="GEMINI_API_KEY")

    # Environment
    environment: str = Field("local", env="APP_ENV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields to be ignored

settings = Settings()
