from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env", override=True)

class Settings(BaseSettings):
    database_url: str

    route_to_call: str

    environment: str

    apk_link: str
    latest_version: str

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding = "utf-8"
    )

    @property
    def database_url(self):
        return self.database_url

settings = Settings()