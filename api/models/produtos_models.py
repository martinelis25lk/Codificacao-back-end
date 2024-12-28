from api.shared.database import Base
from sqlalchemy import Column, Integer, Numeric, String,ForeignKey, DateTime, Boolean


class ProdutoModel(Base):
    __tablename__ = 'produtos'

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    preco = Column(Numeric(10, 2))  # Define precisão e escala para Decimal
    data_de_validade = Column(DateTime())
    categoria = Column(String(30))  # Altere para `Enum(ProdutoCategoriaTipoEnum)` se quiser usar o Enum diretamente
    disponibilidade = Column(Boolean, default=True)
    codigo_de_barras = Column(String(13))
    secao = Column(String(30))
    estoque_inicial = Column(Integer)  # Use Integer em vez de Numeric para quantidade inteira
    imagem = Column(String)  # Armazena a URL da imagem
# ,  estoque inicial, imagens