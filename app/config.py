from pydantic_settings import BaseSettings

class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    # secret key from env
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"  # To ignore any extra keys like flask_env
