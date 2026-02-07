from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., min_length=1)
    OLLAMA_BASE_URL: str = Field('http://localhost:11434')
    OLLAMA_MODEL: str = Field('llama3')
    OLLAMA_VISION_MODEL: str = Field('llava')
    ALLOWED_ORIGINS: str = Field('http://localhost:5173')
    ALLOWED_ORIGIN_REGEX: str = Field('', description='Optional regex for allowed CORS origins')
    APP_ENV: str = Field('local')

    model_config = SettingsConfigDict(env_file='.env', extra='forbid', case_sensitive=False)

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if 'postgres' not in value:
            raise ValueError('DATABASE_URL must be a Postgres URL')
        return value

    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(',') if o.strip()]

    def cors_origin_regex(self) -> str | None:
        value = self.ALLOWED_ORIGIN_REGEX.strip()
        return value or None


settings = Settings()
