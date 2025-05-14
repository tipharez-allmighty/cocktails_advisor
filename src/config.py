import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    DATASET_NAME: str = "final_cocktails.csv"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")


settings = Config()
