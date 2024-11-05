from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from jose import jwt, JWTError
from decouple import config
from models.usuario_model import UserModel
from auth.schemas import User
from jose import jwt, JWTError


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def usuario_register(self, user: User):#user do tipo schema
        user_model = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Usuario já existe'
            )
        
    def usuario_login(self, user: User, expira_em : int = 30):
        usuario_no_bd = self.db_session.query(UserModel).filter_by(username = user.username).first()

        if usuario_no_bd is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuário ou Senha incorretos"
            )
        
        if not crypt_context.verify(user.password, usuario_no_bd.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuário ou Senha incorretos"
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expira_em)

        payload ={
            'sub': user.username,
            'exp': exp
        }

        token_de_acesso = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {'acess_token': token_de_acesso,
                'expiração'  : exp.isoformat()}