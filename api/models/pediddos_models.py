from shared.database import Base
from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, Boolean, DateTime

class PedidoModel(Base):
    __tablename__ = 'pedidos'
    codigo_pedido = Column(Integer, primary_key= True, autoincrement = True)
    periodo = Column(DateTime())
    status_pedido = Column(Boolean, default= True)
    cliente = Column()
    secao_dos_produts = Column(String(45))

    



# período, seção dos produtos, id_pedido, status do pedido e cliente.