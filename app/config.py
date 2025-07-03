from pydantic_settings import BaseSettings
from typing import List
class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    # secret key from env
    SECRET_KEY: str
    JWT_SECRET_KEY:str
   
    # @property
    # def JWT_SECRET_KEY(self) -> str:
    #     print(self.SECRET_KEY)
    #     return self.SECRET_KEY
    JWT_TOKEN_LOCATION: List[str] = ["headers"]
    JWT_HEADER_NAME:str="X-Auth-Token"
    JWT_HEADER_TYPE:str=""

    class Config:
        env_file = ".env"
        extra = "ignore"  # To ignore any extra keys like flask_env
