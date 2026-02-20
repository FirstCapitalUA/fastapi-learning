from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    adult_age: int = 18
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
