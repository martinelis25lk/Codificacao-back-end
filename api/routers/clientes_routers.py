from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from api.autenticacao.funcoes_auxiliares_token import valida_cpf, valida_email, valida_nome_cliente
from fastapi import HTTPException, status
from sqlalchemy import select

from typing import List
from decimal import Decimal
#from api.shared.dependencies import get_db
from api.shared.database import get_session
from sqlalchemy.orm import Session
from api.models.clientes_models import ClienteModel
from typing import List, Optional
import re 




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


@router.post("/cria_cliente", response_model = ClienteResponse) 
def criar_cliente(
    cliente_request : ClienteRequest,
    session = Depends(get_session)):
    

    db_cliente = session.scalar(
        select(ClienteModel).where(ClienteModel.cpf == cliente_request.cpf)
    )
    if db_cliente:
        raise HTTPException(detail='Cliente com este CPF já está cadastrado', status_code=status.HTTP_400_BAD_REQUEST)
    
    
    valida_nome_cliente(cliente_request.nome)
    valida_email(cliente_request.email)
    valida_cpf(cliente_request.cpf)
    
    cliente_a_ser_retornado = ClienteModel(
        **cliente_request.dict()
    )

    
    session.add(cliente_a_ser_retornado)
    session.commit()
    session.refresh(cliente_a_ser_retornado)

    return ClienteResponse(
        **cliente_a_ser_retornado.__dict__
    )
    





@router.get("/listar_com_paginacao", response_model=List[ClienteResponse])
def paginar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    nome: str = Query(None, min_length=1),
    email: str = Query(None, min_length=1),
    session: Session = Depends(get_session)
) -> List[ClienteResponse]:
    
    query = select(ClienteModel)
    
    if nome:
        query = query.where(ClienteModel.nome.ilike(f"%{nome}%"))
    if email:
        query = query.where(ClienteModel.email.ilike(f"%{email}%"))

    clientes = session.scalars(query.offset(skip).limit(limit)).all()

    return clientes
    


@router.get("/pegar_cliente_id/{id_do_cliente}", response_model=ClienteResponse)
def lista_cliente_por_id(
    id_do_cliente: int,
    session: Session = Depends(get_session)
) -> ClienteResponse:
  
    cliente = session.scalar(select(ClienteModel).where(ClienteModel.id == id_do_cliente))

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente




@router.put("/atualizar_cliente_id/{id_do_cliente}", response_model=ClienteResponse, status_code=200)
def atualizar_cliente(
    id_do_cliente: int,
    cliente_request: ClienteRequest,
    session: Session = Depends(get_session)
) -> ClienteResponse:
    
    cliente_db = session.scalar(select(ClienteModel).where(ClienteModel.id == id_do_cliente))
    
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    

    cliente_db.cpf = cliente_request.cpf or cliente_db.cpf
    cliente_db.nome = cliente_request.nome or cliente_db.nome
    cliente_db.email = cliente_request.email or cliente_db.email

    
    session.commit()
    session.refresh(cliente_db)
    
    return cliente_db




@router.delete("/excluir_cliente/{id_do_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(
    id_do_cliente: int,
    session: Session = Depends(get_session)
) -> None:
    
    cliente_db = session.scalar(select(ClienteModel).where(ClienteModel.id == id_do_cliente))
    
    if not cliente_db:
        raise HTTPException(
            detail="Cliente não encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(cliente_db)
    session.commit()

    return {"msg": "Cliente excluído com sucesso"}
 




def buscar_cliente_por_id(id_do_cliente: int, db: Session) -> ClienteResponse:
    cliente_a_ser_retornado = db.query(ClienteModel).get(id_do_cliente)
    if cliente_a_ser_retornado is None:
        raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    

    return cliente_a_ser_retornado

    
