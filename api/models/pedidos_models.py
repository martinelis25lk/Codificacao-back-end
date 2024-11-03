from shared.database import Base
from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class PedidoModel(Base):
    __tablename__ = 'pedidos'
    codigo_pedido = Column(Integer, primary_key= True, autoincrement = True)
    periodo = Column(DateTime())
    status_pedido = Column(Boolean, default= True)
    secao_dos_produtos = Column(String(45))
    id_do_cliente = Column(Integer, ForeignKey("clientes.id"))#relação one to many sql alchemy, 
    cliente = relationship("ClienteModel")


    #cliente é o pai, e os pedidos é o filho 
    

    



# período, seção dos produtos, id_pedido, status do pedido e cliente.