import os


class SettingConnect:
    """str for connection to db"""

    DB_HOST: str | None = os.environ.get('DB_HOST')
    DB_USER: str | None = os.environ.get('DB_USER')
    DB_PASS: str | None = os.environ.get('DB_PASS')
    DB_NAME: str | None = os.environ.get('DB_NAME')
    DB_PORT: str | None = os.environ.get('DB_PORT')

    @property
    def ASYNC_CONNECTION(self) -> str:
        return f'postgresql+ayncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


db_string = SettingConnect()
