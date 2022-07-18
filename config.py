from typing import List
import os


class Config:
    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    TRUSTED_IDS: List[int] = [int(i) for i in os.getenv('TRUSTED_IDS').split(" ")]
