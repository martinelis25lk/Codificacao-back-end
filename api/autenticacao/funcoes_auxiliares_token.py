from datetime import datetime, timedelta
from pwdlib import PasswordHash
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from api.shared.database import get_session
from sqlalchemy import select
from api.models.usuario_model import UserModel
from jwt.exceptions import PyJWTError
from fastapi import HTTPException, status



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

    #adiciona um tempo de 30 minutos para exibição
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

        
    usuario_bd = session.scalar(select(UserModel).where(UserModel.username == username))

    if not usuario_bd:
        raise credentials_exception
    

    return usuario_bd
        
         
  


    
    

 


