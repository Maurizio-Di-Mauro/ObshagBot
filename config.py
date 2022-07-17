import os


class Config:
    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    TRUSTED_IDS = os.getenv('TRUSTED_IDS')