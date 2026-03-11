import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("X_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///bestphone.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_EXPIRY_HOURS = int(os.getenv("CACHE_EXPIRY_HOURS", 24))
