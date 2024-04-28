from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_user: str = Field(
        default="postgres_user",
        description="Имя пользователя Postgres для модуля оповещений",
    )
    postgres_pass: str = Field(
        default="postgres_pass",
        description="Пароль пользователя Postgres для модуля оповещений",
    )
    postgres_host: str = Field(
        default="postgres_auth",
        description="Адрес хоста Postgres для модуля оповещений",
    )
    postgres_port: int = Field(
        default=5432,
        description="Порт Postgres для сервиса оповещений",
    )
    postgres_database: str = Field(
        default="base",
        description="База данных для хранения информации об оповещениях",
    )

    @property
    def conn_url(self):
        return (
            f'postgresql+psycopg2://'
            f'{self.postgres_user}:{self.postgres_pass}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}'
        )

class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



settings = Settings()
