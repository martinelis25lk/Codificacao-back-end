from datetime import datetime, timedelta
from pwdlib import PasswordHash
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from api.shared.database import get_session
from api.models.clientes_models import ClienteModel
from sqlalchemy import select
from api.models.usuario_model import UsuarioModel
from jwt.exceptions import PyJWTError
from fastapi import HTTPException, status
import re



SECRET_KEY = 'your-secret-key'
ALGORITHM  = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()

oaut2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/token")

def obtem_senha_hash(password : str):
    return pwd_context.hash(password)


def verifica_senha(plain_password: str, hashed_password: str):
    return  pwd_context.verify(plain_password, hashed_password)


def criar_token_de_acesso(data : dict):#data sao as coisas q vao estar dentro do payload
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt




def obtem_usuario_atual(
    session: Session = Depends(get_session),
    token : str = Depends(oaut2_scheme),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='could not validate credentials',
        headers={' WWW-Authenticate':'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub') #username do formulario
        if not username:
            raise credentials_exception

    except PyJWTError:
           raise credentials_exception

        
    usuario_bd = session.scalar(select(UsuarioModel).where(UsuarioModel.username == username))

    if not usuario_bd:
        raise credentials_exception
    

    return usuario_bd
        
         
  
def valida_email(email : str):
    email_regex = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email): 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido. Insira um e-mail em formato válido"
        )



def valida_cpf(cpf : str):
    if len(cpf) < 11 or not cpf.isdigit():
        raise HTTPException(
            status_code=400,
            detail="CPF inválido. o CPF deve conter exatamente 11 digitos numéricos"
        )




def valida_nome_cliente(nome : str):
    if len(nome)> 30:
        raise HTTPException(
            status_code = 400,
            detail='Nome de usuário muito grande.'
        
        )








 


