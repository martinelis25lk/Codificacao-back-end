from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import List
from decimal import Decimal
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from models.pedidos_models import PedidoModel 
from typing import List, Optional
from shared.dependencies import usuario_validacao, admin_validacao







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


    

@router.post("", response_model=PedidoResponse,dependencies=[Depends(admin_validacao)])
def criar_pedido(pedido_request : PedidoRequest ,db:Session = Depends(get_db))-> PedidoResponse:
    pedido_a_ser_criado = PedidoModel(**pedido_request.model_dump())
    db.add(pedido_a_ser_criado)
    db.commit()
    db.refresh(pedido_a_ser_criado)

    return pedido_a_ser_criado
    

@router.get("/{id_do_pedido}", response_model=PedidoResponse,dependencies=[Depends(usuario_validacao)])
def listar_pedido_pelo_id(id_do_pedido : int, db: Session = Depends(get_db))-> PedidoResponse:
    pedido_a_ser_retornado = db.query(PedidoModel).get(id_do_pedido)
    return pedido_a_ser_retornado


@router.delete("/{id_do_pedido}", response_model=None,dependencies=[Depends(admin_validacao)])
def excluir_pedido(id_do_pedido : int, db:Session= Depends(get_db))-> None:
    pedido_a_ser_deletado = db.query(PedidoModel).get(id_do_pedido)

    db.delete(pedido_a_ser_deletado)
    db.commit()



@router.get("/paginacao", response_model=List[PedidoResponse],dependencies=[Depends(usuario_validacao)])
def paginar_pedidos(page              : int = Query(1, ge=1),
                    page_size          : int = Query(10, ge=1, le=100),
                    secao_dos_produtos : str =   Query(None, min_length= 1),
                    status_pedido      : bool =  Query(None),
                    

                    db: Session = Depends(get_db)):
    
    query = db.query(PedidoModel)
    
    if secao_dos_produtos:
        query = query.filter(PedidoModel.secao_dos_produtos.ilike(f"%{secao_dos_produtos}%"))
    if status_pedido:
        query = query.filter(PedidoModel.status_pedido == status_pedido)

    
    skip = (page -1 )* page_size # calcula o indice inicial
    pedidos = query.offset(skip).limit(page_size).all()

    return pedidos


@router.put("/{id_do_pedido}", response_model=PedidoResponse,dependencies=[Depends(admin_validacao)])
def atualizar_pedido(id_do_pedido : int, pedido_request : PedidoRequest, db : Session = Depends(get_db))->PedidoResponse:
    pedido_a_ser_atualizado = buscar_pedido_por_id(id_do_pedido, db)
    pedido_a_ser_atualizado.status_pedido = pedido_request.status_pedido
    pedido_a_ser_atualizado.secao_dos_produtos = pedido_request.secao_dos_produtos
    pedido_a_ser_atualizado.periodo = pedido_request.periodo

    db.add(pedido_a_ser_atualizado)
    db.commit()
    db.refresh(pedido_a_ser_atualizado)

    return pedido_a_ser_atualizado



    
    
    



def buscar_pedido_por_id(id_do_pedido: int, db: Session,dependencies=[Depends(usuario_validacao)]) -> PedidoResponse:
    pedido_a_ser_retornado = db.query(PedidoModel).get(id_do_pedido)
    if pedido_a_ser_retornado is None:
        raise("pedido nao existe.")
    

    return pedido_a_ser_retornado
