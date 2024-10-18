from shared.database import Base
from sqlalchemy import Column, Integer, Numeric, String,ForeignKey, DateTime, Boolean


class ProdutoModel(Base):
    __tablename__= 'produtos'
    codigo = Column(Integer, primary_key = True, autoincrement= True)
    descricao = Column(String(30))
    preco = Column(Numeric)
    data_de_validade = Column(DateTime())
    categoria = Column(String(30))
    disponibilidade = Column(Boolean, default = True)
    codigo_de_barras = Column(String(13))
    secao = Column(String)
    estoque_inicial = Column(Numeric)
    imagem = Column(String)  # Armazena a URL da imagem




# ,  estoque inicial, imagens