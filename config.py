"""
Configurações do Music-Makro
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Informações do App
    APP_NAME: str = "Music-Makro"
    APP_VERSION: str = "1.0.0"
    
    # Segurança JWT
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_USE_STRONG_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 20
    RATE_LIMIT_PER_HOUR: int = 200
    
    # CORS (domínios permitidos)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Usuários API (formato: username:password_hash)
    API_USERS: str = ""
    
    # Paths
    TEMP_DIR: str = "temp"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_allowed_origins(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    def get_api_users(self) -> dict:
        """Retorna dicionário de usuários {username: password_hash}"""
        users = {}
        if self.API_USERS:
            for user_line in self.API_USERS.split(","):
                if ":" in user_line:
                    username, password_hash = user_line.split(":", 1)
                    users[username.strip()] = password_hash.strip()
        return users
    
    def ensure_temp_dir(self):
        """Garante que diretório temporário existe"""
        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)

settings = Settings()