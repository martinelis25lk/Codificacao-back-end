from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query

from typing import List
from decimal import Decimal
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from models.clientes_models import ClienteModel
from typing import List, Optional



router = APIRouter(prefix="/clientes")

class ClienteResponse(BaseModel):
    id    : int
    cpf   : str
    nome  : str
    email : str


class ClienteRequest(BaseModel):
    cpf   : str
    nome  : str
    email : str




@router.post("", response_model = ClienteResponse) 
def criar_cliente(cliente_request : ClienteRequest,
                   db : Session = Depends(get_db))-> ClienteResponse:
    
    cliente_a_ser_retornado = ClienteModel(
        **cliente_request.dict()
    )
    
    db.add(cliente_a_ser_retornado)
    db.commit()
    db.refresh(cliente_a_ser_retornado)

    return ClienteResponse(
        **cliente_a_ser_retornado.__dict__
    )
    





@router.get("/paginacao", response_model=List[ClienteResponse])
def paginar_clientes(page: int = Query(1, ge=1),
                    page_size: int = Query(10, ge=1, le=100),
                    nome : str = Query(None, min_length=1),
                    email : str =   Query(None, min_length= 1),
                    db: Session = Depends(get_db)):
    
    query = db.query(ClienteModel)
    
    if nome:
        query = query.filter(ClienteModel.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(ClienteModel.email.ilike(f"%{email}%"))
    
    skip = (page -1 )* page_size # calcula o indice inicial
    clientes = query.offset(skip).limit(page_size).all()

    return clientes

    




@router.delete("/{id_do_cliente}", status_code= 204)
def excluir_cliente(id_do_cliente : int, 
                    db: Session = Depends(get_db))-> None:
    cliente = db.query(ClienteModel).get(id_do_cliente)


    db.delete(cliente)
    db.commit()

 


    

@router.get("/{id_do_cliente}", response_model=ClienteResponse)
def lista_cliente_por_id(id_do_cliente: int,
                          db: Session = Depends(get_db))-> ClienteResponse:
    return buscar_cliente_por_id(id_do_cliente, db)




@router.put("/{id_do_cliente}", response_model = ClienteResponse, status_code=200)
def atualizar_cliente(id_do_cliente : int,
                      cliente_request : ClienteRequest,
                      db: Session = Depends(get_db))-> ClienteResponse:
    cliente_atualizado = buscar_cliente_por_id(id_do_cliente, db)
    cliente_atualizado.cpf = cliente_request.cpf
    cliente_atualizado.nome = cliente_request.nome
    cliente_atualizado.email = cliente_request.email

    db.add(cliente_atualizado)
    db.commit()
    db.refresh(cliente_atualizado)

    return cliente_atualizado



def buscar_cliente_por_id(id_do_cliente: int, db: Session) -> ClienteResponse:
    cliente_a_ser_retornado = db.query(ClienteModel).get(id_do_cliente)
    if cliente_a_ser_retornado is None:
        raise("cliente nao existe.")
    

    return cliente_a_ser_retornado


