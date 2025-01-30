from api.shared.database import Base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship


class ClienteModel(Base):
    __tablename__= 'clientes'
    id = Column(Integer, primary_key = True, autoincrement = True)
    cpf = Column(String(11))
    email = Column(String(30))
    nome = Column(String(30))

 







#nome, email, cpf, id