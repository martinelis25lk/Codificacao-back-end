from pydantic import BaseModel
from fastapi import APIRouter, Depends
from typing import List
from decimal import Decimal
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from models.clientes_models import Clientes



router = APIRouter(prefix="/magazine")

class ClienteResponse(BaseModel):
    id    : int
    cpf   : str
    nome  : str
    email : str


class ClienteRequest(BaseModel):
    cpf   : str
    nome  : str
    email : str




@router.post("/clients", response_model = ClienteResponse) 
def criar_cliente(cliente_request : ClienteRequest,
                   db : Session = Depends(get_db))-> ClienteResponse:
    
    cliente_a_ser_retornado = Clientes(
        **cliente_request.dict()
    )
    
    db.add(cliente_a_ser_retornado)
    db.commit()
    db.refresh(cliente_a_ser_retornado)

    return ClienteResponse(
        **cliente_a_ser_retornado.__dict__
    )
    



@router.get("/clients", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db))-> List[ClienteResponse]:
    clientes = db.query(Clientes).all()
    return clientes





@router.delete("/clients/{id_do_cliente}", status_code= 204)
def excluir_cliente(id_do_cliente : int, 
                    db: Session = Depends(get_db))-> None:
    cliente = db.query(Clientes).get(id_do_cliente)


    db.delete(cliente)
    db.commit()

 


    

@router.get("clients/{id_do_cliente}", response_model=ClienteResponse)
def listar_cliente_por_id(id_do_cliente: int,
                          db: Session = Depends(get_db))-> ClienteResponse:
    return buscar_cliente_por_id(id_do_cliente, db)





def buscar_cliente_por_id(id_do_cliente: int, db: Session) -> ClienteResponse:
    cliente_a_ser_retornado = db.query(Clientes).get(id_do_cliente)
    if cliente_a_ser_retornado is None:
        raise("cliente nao existe.")
    

    return cliente_a_ser_retornado






@router.put("/clients/{id_do_cliente}", response_model = ClienteResponse, status_code=200)
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



