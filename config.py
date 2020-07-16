"""App configuration."""
import os

class Config:
    """Set Flask configuration vars."""

    # General Config
    ENV = os.environ.get("APP_ENV", "development")
    DEBUG = os.environ.get("APP_DEBUG", True)
    SECRET_KEY= os.environ.get("SECRET_KEY", "you_will_never_guess")

    # Database
    DB_NAME = os.environ.get("DB_NAME", 'cookbook')
    DB_HOST = os.environ.get("DB_HOST", 'localhost')
    DB_PORT = int(os.environ.get("DB_PORT", 27000))
    DB_USER = os.environ.get("DB_USER", 'root')
    DB_PASSWORD = os.environ.get("DB_PASSWORD", 'admin')
    AUTHENTICATION_SOURCE = os.environ.get("AUTHENTICATION_SOURCE", 'admin')

    # Imgur
    IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")