# import os
# from pydantic import  BaseSettings
#
# class Settings(BaseSettings):
#     APP_NAME: str = "FastApi Food Api"
#     DEBUG: bool = False
#     MONGO_URI: str
#     MONGO_DB: str = "food_db"
#     JWT_SECRET: str
#     JWT_ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
#
#     class Config:
#         env_file = ".env"
#
# settings = Settings()