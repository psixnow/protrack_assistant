import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: List[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///database.db")
    
    def get_admin_ids(self) -> List[int]:
        return self.ADMIN_IDS

settings = Settings()