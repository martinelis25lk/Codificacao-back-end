from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from typing import List
from decimal import Decimal
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from models.produtos_models import ProdutoModel
from typing import List, Optional
from datetime import datetime




#categoria, preço, disponibilidade, descricao, valor de venda, codigo de barras, seção, estoque inicial, data de validade, imagens


router = APIRouter(prefix="/produtos")



class ProdutoCategoriaTipoEnum(str, Enum):
    MOVEIS =      'moveis'
    MEDICAMENTO = 'medicamento'
    ELETRONICOS = 'eletronicos'




class ProdutoResponse(BaseModel):
    codigo           : int
    descricao        : str
    preco            : Decimal
    data_de_validade : datetime   
    categoria        : ProdutoCategoriaTipoEnum
    disponibilidade  : bool
    codigo_de_barras : str
    secao            : str
    estoque_inicial  : int
    imagem           : str









class ProdutoRequest(BaseModel):
    descricao        : str
    preco            : Decimal
    data_de_validade : datetime   
    categoria        : ProdutoCategoriaTipoEnum
    disponibilidade  : bool
    codigo_de_barras : str
    secao            : str
    estoque_inicial  : int
    imagem           : str







