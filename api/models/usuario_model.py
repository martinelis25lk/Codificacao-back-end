from sqlalchemy import Column, String, Integer
from shared.database import Base

#representa modelo de tabela no bd
class UserModel(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    cargo = Column(String, default='usuario')  # 'admin' ou 'user'