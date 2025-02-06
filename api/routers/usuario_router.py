from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select
from api.models.usuario_model import UsuarioModel
from typing import List
import re 
from fastapi.security import OAuth2PasswordRequestForm
from api.autenticacao.funcoes_auxiliares_token import (
    verifica_senha, 
    obtem_senha_hash, 
    criar_token_de_acesso,
    obtem_usuario_atual,)

from api.autenticacao.schemas import Token
from api.shared.database import get_session




router = APIRouter(prefix='/usuarios')




class UsuarioResponse(BaseModel):
    id        : int
    username  : str
    password  : str
    cargo     : str

    class Config:
        from_attributes = True  # Permitir o uso de from_orm()
   



class UsuarioRequest(BaseModel):
    username  : str
    password  : str
    cargo     : str




@router.post('/cria_usuario', status_code=status.HTTP_201_CREATED, response_model=UsuarioResponse)
def criar_usuario(
    usuario : UsuarioRequest, 
    session = Depends(get_session),
    ):
                  
    db_usuario = session.scalar(
        select(UsuarioModel).where(
            UsuarioModel.username == usuario.username
        )
    )
                  
    if db_usuario:
        raise HTTPException(
            detail='usuario com esse username ja cadastrado', status_code=status.HTTP_400_BAD_REQUEST
        )
    
    usuario_a_ser_retornado = UsuarioModel(
       username = usuario.username,
       password = obtem_senha_hash(usuario.password), # senha suja
       cargo    = usuario.cargo
       )

    session.add(usuario_a_ser_retornado)
    session.commit()
    session.refresh(usuario_a_ser_retornado)

    return UsuarioResponse(
        **usuario_a_ser_retornado.__dict__
    )




@router.get('/listar_usuarios', response_model=list[UsuarioResponse])
def listar_usuarios(
        skip: int = 0, limit : int = 100, session: Session = Depends(get_session)):
    usuarios = session.scalars(select(UsuarioModel).offset(skip).limit(limit)).all()

    return usuarios



@router.delete('/deletar_usuario/{usuario_id}')
def deletar_usuario(
    usuario_id: int,
    usuario_atual = Depends(obtem_usuario_atual),
    session : Session = Depends(get_session)
    ):

    if usuario_atual.id != usuario_id:
        raise HTTPException(
        detail='permissoes insuficientes',
        status_code=status.HTTP_400_BAD_REQUEST
    )

    session.delete(usuario_atual)
    session.commit()

    return {'msg': 'usuario deletado'}
    
    




@router.put('/atualizar_usuario/{usuario_id}', response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioRequest,
    usuario_atual = Depends(obtem_usuario_atual), 
    session: Session = Depends(get_session)
    ):



    usuario_db = session.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


    if usuario_atual.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='permissões insuficientes' 
        )



    usuario_db.username = usuario.username
    usuario_db.password = obtem_senha_hash(usuario.password)
    usuario_db.cargo    = usuario.cargo


    session.commit()
    session.refresh(usuario_db) 

    return usuario_db










@router.post('/token', response_model=Token)
def login_para_o_token_de_acesso(
    form_data : OAuth2PasswordRequestForm = Depends(), 
    session : Session = Depends(get_session),
):
    
    usuario = session.scalar(select(UsuarioModel).where(UsuarioModel.username == form_data.username))
    
    

    if not usuario or not verifica_senha(form_data.password, usuario.password):
        raise HTTPException(
            status_code=400, detail='nome de usuario ou senha incorreto...usuario router'
        )
    

    token_de_acesso = criar_token_de_acesso(data={'sub': usuario.username})

    return {'token_de_acesso': token_de_acesso, 'tipo_de_token': 'Bearer'}

        
     
    




