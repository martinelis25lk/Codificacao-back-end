from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import List
from decimal import Decimal
from api.shared.database import get_session
from sqlalchemy.orm import Session
from api.models.pedidos_models import PedidoModel 
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import select

from api.models.clientes_models import ClienteModel








router = APIRouter(prefix="/pedidos")

class PedidoRequest(BaseModel):
    status_pedido      : bool
    secao_dos_produtos : str
    id_do_cliente      : int
    periodo            : datetime


class PedidoResponse(BaseModel):
    codigo_pedido      : int
    status_pedido      : bool
    secao_dos_produtos : str
    id_do_cliente      : int
    periodo            : datetime


    
@router.post("/criar_pedido", response_model=PedidoResponse)
def criar_pedido(
    pedido_request : PedidoRequest,
    session = Depends(get_session))-> PedidoResponse:

    cliente_existente = session.scalar(
        select(ClienteModel).where(
            ClienteModel.id == pedido_request.id_do_cliente
        ))
    
    if not cliente_existente:
        raise HTTPException(
            detail="o cliente selecionado para este pedido não existe na base de dados.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    pedido_a_ser_criado = PedidoModel(**pedido_request.model_dump())
    session.add(pedido_a_ser_criado)
    session.commit()
    session.refresh(pedido_a_ser_criado)

    return pedido_a_ser_criado



@router.get("/listar_pedido/{id_do_pedido}", response_model=PedidoResponse)
def listar_pedido_pelo_id(
    id_do_pedido: int, 

    session: Session = Depends(get_session)
) -> PedidoResponse:
    

    pedido_a_ser_retornado = session.scalar(
        select(PedidoModel).where(PedidoModel.codigo_pedido == id_do_pedido)
    )

    if not pedido_a_ser_retornado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido_a_ser_retornado


@router.delete("/excluir_pedido/{id_do_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pedido(
    id_do_pedido: int, 
    session: Session = Depends(get_session)
) -> None:
    pedido_a_ser_deletado = session.scalar(
        select(PedidoModel).where(PedidoModel.codigo_pedido  == id_do_pedido)
    )

    if not pedido_a_ser_deletado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    session.delete(pedido_a_ser_deletado)
    session.commit()

    


@router.get("/listar/paginacao", response_model=List[PedidoResponse])
def paginar_pedidos(
    skip: int = 0,
    limit: int = 10,
    secao_dos_produtos: Optional[str] = Query(None, min_length=1),
    status_pedido: Optional[bool] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(PedidoModel)

    if secao_dos_produtos:
        query = query.where(PedidoModel.secao_dos_produtos.ilike(f"%{secao_dos_produtos}%"))

    if status_pedido is not None:
        query = query.where(PedidoModel.status_pedido == status_pedido)

    pedidos = session.scalars(query.offset(skip).limit(limit)).all()

    return pedidos







@router.put("/atualizar_pedido/{id_do_pedido}", response_model=PedidoResponse)
def atualizar_pedido(
    id_do_pedido: int, 
    pedido_request: PedidoRequest, 
    session: Session = Depends(get_session)
) -> PedidoResponse:
    
    pedido_a_ser_atualizado = session.scalar(
        select(PedidoModel).where(PedidoModel.codigo_pedido == id_do_pedido)
    )

    if not pedido_a_ser_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido_a_ser_atualizado.status_pedido = pedido_request.status_pedido
    pedido_a_ser_atualizado.secao_dos_produtos = pedido_request.secao_dos_produtos
    pedido_a_ser_atualizado.periodo = pedido_request.periodo

    session.commit()
    session.refresh(pedido_a_ser_atualizado)

    return pedido_a_ser_atualizado

    



def buscar_pedido_por_id(id_do_pedido: int, db: Session) -> PedidoResponse:
    pedido_a_ser_retornado = db.query(PedidoModel).get(id_do_pedido)
    if pedido_a_ser_retornado is None:
        raise("pedido nao existe.")
    

    return pedido_a_ser_retornado
