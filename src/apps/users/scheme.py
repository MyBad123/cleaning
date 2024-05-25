from pydantic import BaseModel


class UserRequest(BaseModel):
    """user update request fields"""

    phone: int | None = None
    name: str | None = None
    sername: str | None = None
    patronymic: str | None = None
    inn: int | None = None
    mail: str | None = None
