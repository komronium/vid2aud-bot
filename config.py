from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_USERNAME: str
    CHANNEL_JOIN_LINK: str
    GROUP_ID: int

    class Config:
        env_file = '.env'


settings = Settings()
