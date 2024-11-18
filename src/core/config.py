from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import pytz

load_dotenv()


class Settings(BaseSettings):
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_HOSTNAME: str
    ACTUAL_TIMEZONE: str

    CLIENT_ORIGIN: str
    SL_API_PASSWORD: str
    SL_API_SALT: str

    class Config:
        env_file = "./.env"

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.ACTUAL_TIMEZONE)

    @property
    def timezone_pytz(self):
        return pytz.timezone(self.ACTUAL_TIMEZONE)


settings = Settings()
