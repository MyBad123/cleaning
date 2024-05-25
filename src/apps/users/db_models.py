import email_validator
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import validates
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, String, Integer


BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[int]
    name: Mapped[str] = Column(String, nullable=True)
    sername: Mapped[str] = Column(String, nullable=True)
    patronymic: Mapped[str] = Column(String, nullable=True)
    inn: Mapped[int] = Column(Integer, nullable=True)
    mail: Mapped[str] = Column(String, nullable=True)

    @validates('mail')
    def validates_mail(self, key, value):
        email_validator.validate_email(value)
        return value
