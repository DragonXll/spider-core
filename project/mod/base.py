from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """ 基类表 """
    __name__: str

    __table_args__ = {'mysql_charset': 'utf8', 'extend_existing': True}

    __mapper_args__ = {'eager_defaults': True}

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


