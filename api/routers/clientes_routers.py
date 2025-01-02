from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query

from fastapi import HTTPException, status

from typing import List
from decimal import Decimal
from api.shared.dependencies import get_db
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
def criar_cliente(cliente_request : ClienteRequest,
                   db : Session = Depends(get_db))-> ClienteResponse:
    

    cliente_existente = db.query(ClienteModel).filter(ClienteModel.cpf == cliente_request.cpf).first()
    if cliente_existente:
        raise HTTPException(detail='Cliente com este CPF já está cadastrado', status_code=status.HTTP_400_BAD_REQUEST)
    
    
    valida_nome_cliente(cliente_request.nome)
    valida_email(cliente_request.email)
    valida_cpf(cliente_request.cpf)
    
    cliente_a_ser_retornado = ClienteModel(
        **cliente_request.dict()
    )

    
    db.add(cliente_a_ser_retornado)
    db.commit()
    db.refresh(cliente_a_ser_retornado)

    return ClienteResponse(
        **cliente_a_ser_retornado.__dict__
    )
    





@router.get("/listar_com_paginacao", response_model=List[ClienteResponse])
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

    


@router.get("/pegar_cliente_id/{id_do_cliente}", response_model=ClienteResponse)
def lista_cliente_por_id(id_do_cliente: int,
                          db: Session = Depends(get_db))-> ClienteResponse:
    cliente = db.query(ClienteModel).get(id_do_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
    #return buscar_cliente_por_id(id_do_cliente, db)





@router.put("/atualizar_cliente_id/{id_do_cliente}", response_model = ClienteResponse, status_code=200)
def atualizar_cliente(id_do_cliente : int,
                      cliente_request : ClienteRequest,
                      db: Session = Depends(get_db))-> ClienteResponse:
    cliente_atualizado = buscar_cliente_por_id(id_do_cliente, db)

    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')

     # Atualiza apenas os campos enviados na requisição
    cliente_atualizado.cpf = cliente_request.cpf or cliente_atualizado.cpf
    cliente_atualizado.nome = cliente_request.nome or cliente_atualizado.nome
    cliente_atualizado.email = cliente_request.email or cliente_atualizado.email


    db.add(cliente_atualizado)
    db.commit()
    db.refresh(cliente_atualizado)

    return cliente_atualizado





@router.delete("/excluir_cliente/{id_do_cliente}", status_code= 204)
def excluir_cliente(id_do_cliente : int, 
                    db: Session = Depends(get_db))-> None:
    cliente = db.query(ClienteModel).get(id_do_cliente)

    if not cliente:
        raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)


    db.delete(cliente)
    db.commit()

 






#funções auxiliares para as rotas

def buscar_cliente_por_id(id_do_cliente: int, db: Session) -> ClienteResponse:
    cliente_a_ser_retornado = db.query(ClienteModel).get(id_do_cliente)
    if cliente_a_ser_retornado is None:
        raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
    

    return cliente_a_ser_retornado


def valida_nome_cliente(nome : str):
    if len(nome)> 30:
        raise HTTPException(
            status_code = 400,
            detail='Nome de usuário muito grande.'
        
        )

def valida_cpf(cpf : str):
    if len(cpf) < 11 or not cpf.isdigit():
        raise HTTPException(
            status_code=400,
            detail="CPF inválido. o CPF deve conter exatamente 11 digitos numéricos"
        )

def valida_email(email : str):
    email_regex = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido. Insira um e-mail em formato válido"
        )

    
