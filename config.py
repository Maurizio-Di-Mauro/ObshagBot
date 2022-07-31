import os


class Config:
    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    TRUSTED_IDS = [int(i) for i in os.getenv('TRUSTED_IDS').split(" ")]

    NUMBER_OF_LAST_EXPENSES: int = os.getenv('NUMBER_OF_LAST_EXPENSES') or 10

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
