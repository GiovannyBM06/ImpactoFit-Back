"""
config.py
---------
Configuración centralizada del proyecto usando pydantic-settings.

pydantic-settings lee automáticamente las variables del archivo .env
y las valida con tipos estrictos. Si una variable obligatoria falta,
lanza un error descriptivo al iniciar la aplicación (fail fast).

Uso:
    from core.config import settings
    print(settings.DATABASE_URL)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Variables de entorno del proyecto.

    Todas las variables se leen desde el archivo .env en la raíz del proyecto.
    Los nombres son case-insensitive (DATABASE_URL == database_url en el .env).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Base de datos (NeonDB / PostgreSQL) ──────────────────────────────────
    # Formato: postgresql://usuario:password@host/nombre_bd?sslmode=require
    # La URL completa se obtiene en: NeonDB Dashboard → Connection Details
    DATABASE_URL: str

    # ── Email (SMTP) ──────────────────────────────────────────────────────────
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"

    # ── JWT ──────────────────────────────────────────────────────────────────
    # Clave secreta para firmar los tokens. Debe ser larga y aleatoria.
    # Generar con: openssl rand -hex 32
    SECRET_KEY: str

    # Algoritmo de firma del JWT (HS256 es el estándar para APIs REST)
    ALGORITHM: str = "HS256"

    # Tiempo de expiración del token en minutos (default: 8 horas)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # ── Aplicación ────────────────────────────────────────────────────────────
    APP_NAME: str = "ImpactoFit API"
    DEBUG: bool = False
    
    FRONTEND_URL: str = "http://localhost:3000"

# Instancia única — se importa en toda la aplicación
# Singleton implícito: Python cachea los módulos, por lo que
# esta instancia se crea una sola vez durante el ciclo de vida
settings = Settings()