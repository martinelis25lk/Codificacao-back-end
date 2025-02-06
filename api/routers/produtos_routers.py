from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query,  HTTPException, status
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from api.models.produtos_models import ProdutoModel
from typing import List, Optional
from datetime import datetime
from api.shared.database import get_session
from sqlalchemy import select











#categoria, preço, disponibilidade, descricao, valor de venda, codigo de barras, seção, estoque inicial, data de validade, imagens


router = APIRouter(prefix="/produtos")



class ProdutoCategoriaTipoEnum(str, Enum):
    MEDICAMENTO = "medicamento"
    ALIMENTO = "alimento"
    OUTROS = "outros"

# Modelo Pydantic para resposta de produto
class Produto_Response(BaseModel):
    codigo: int
    descricao: str
    preco: Decimal
    data_de_validade: datetime
    categoria: ProdutoCategoriaTipoEnum
    disponibilidade: bool
    codigo_de_barras: str
    secao: str
    estoque_inicial: int
    imagem: str



class Produto_Request(BaseModel):
    descricao        : str
    preco            : Decimal
    data_de_validade : datetime                                    
    categoria        : ProdutoCategoriaTipoEnum
    disponibilidade  : bool
    codigo_de_barras : str
    secao            : str
    estoque_inicial  : int
    imagem           : str



@router.post("/criar_produto", response_model=Produto_Response)
def ciar_produto(
    produto_request : Produto_Request,
    session: Session = Depends(get_session))-> Produto_Response:


    produto_a_ser_criado = ProdutoModel(**produto_request.model_dump())


    session.add(produto_a_ser_criado)
    session.commit()
    session.refresh(produto_a_ser_criado)

    return produto_a_ser_criado




@router.get("/listar_produto_por_id/{id_do_produto}", response_model=Produto_Response)
def listar_produto_por_id(
    id_do_produto: int,
    session: Session = Depends(get_session))-> Produto_Response:
    return buscar_produto_por_id(id_do_produto, session)







@router.get("/produtos_paginacao", response_model=List[Produto_Response])
def listar_produtos_com_paginacao(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    categoria: Optional[str] = Query(None, min_length=1),
    preco: Optional[Decimal] = Query(None),
    disponibilidade: Optional[bool] = Query(None),
    session: Session = Depends(get_session)
):
    query = select(ProdutoModel)

    if categoria:
        query = query.where(ProdutoModel.categoria.ilike(f"%{categoria}%"))

    if preco:
        query = query.where(ProdutoModel.preco == preco)

    if disponibilidade is not None:
        query = query.where(ProdutoModel.disponibilidade == disponibilidade)

    # Paginação
    query = query.offset((page - 1) * page_size).limit(page_size)

    # Executando a consulta
    produtos = session.scalars(query).all()

    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum produto encontrado com os critérios fornecidos."
        )

    return produtos




@router.delete("/excluir_produto/{id_do_produto}")
def excluir_produto(
    id_do_produto: int, 
    session :Session= Depends(get_session))-> None:

    produto_existente = session.scalar(select(ProdutoModel).where(ProdutoModel.codigo == id_do_produto))

    

    if not produto_existente:
        raise HTTPException(
            detail=f'O produto de codigo {id_do_produto} não existe.',
            status_code=status.HTTP_404_NOT_FOUND
        )

    produto_a_ser_excluido = session.query(ProdutoModel).get(id_do_produto)

    session.delete(produto_a_ser_excluido)
    session.commit()



@router.put("/atualizar_produto/{id_do_produto}", response_model= Produto_Response)
def atualizar_produto(
    id_do_produto: int,
    produto_request : Produto_Request,
    session:Session = Depends(get_session))-> Produto_Response:
    
    produto_a_ser_alterado = buscar_produto_por_id(id_do_produto, session)

    produto_a_ser_alterado.descricao        = produto_request.descricao
    produto_a_ser_alterado.data_de_validade = produto_request.data_de_validade
    produto_a_ser_alterado.codigo_de_barras = produto_request.codigo_de_barras
    produto_a_ser_alterado.categoria        =  produto_request.categoria
    produto_a_ser_alterado.disponibilidade  = produto_request.disponibilidade 
    produto_a_ser_alterado.estoque_inicial  = produto_request.estoque_inicial
    produto_a_ser_alterado.imagem           = produto_request.imagem
    produto_a_ser_alterado.secao            = produto_request.secao
    produto_a_ser_alterado.preco            = produto_request.preco

    
    session.add(produto_a_ser_alterado)
    session.commit()
    session.refresh(produto_a_ser_alterado)

    return produto_a_ser_alterado
     

      



def buscar_produto_por_id(
        id_do_produto: int, 
        session: Session) -> Produto_Response:
    

    stmt = select(ProdutoModel).where(ProdutoModel.codigo == id_do_produto)
    produto_a_ser_retornado = session.scalar(stmt)

    if produto_a_ser_retornado is None:
        raise HTTPException(
            detail=f"o produto de codigo {id_do_produto} não existe",
             status_code=status.HTTP_404_NOT_FOUND)

    return produto_a_ser_retornado


