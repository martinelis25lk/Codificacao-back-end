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



SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
    def registrar_usuario(self, user: User):
        user_model = UserModel(
            username = user.username,
            password = crypt_context.hash(user.password),
            cargo = user.cargo
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail='usuario ja existe no banco'
            )
    

    def usuario_login(self, user: User, expira_em : int = 30):
        usuario_no_bd = self.db_session.query(UserModel).filter_by(username = user.username).first()

        if usuario_no_bd is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou Senha incorretos'
            )
        
        if not crypt_context.verify(user.password, usuario_no_bd.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou Senha incorretos'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expira_em)

        payload ={
            'sub': user.username,
            'exp': exp,
            'cargo': usuario_no_bd.cargo,
        }

        token_de_acesso = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {'token_de_acesso': token_de_acesso,
                'expiração'  : exp.isoformat()
                }
    

    def refresh_user_token(self, token: str):
        try:
            # Decodificar o token recebido
            print(f"Token recebido para refresh: {token}")  # Log do token recebido
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")


            if username is None:
                print("Erro: Campo 'sub' ausente no token.")  # Log de erro
                raise HTTPException(
                      status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Token inválido ou expirado",
                )

            # Verificar se o usuário ainda existe no banco
            usuario_no_bd = self.db_session.query(UserModel).filter_by(username=username).first()
            if usuario_no_bd is None:
               print(f"Usuário {username} não encontrado no banco de dados.")  # Log de erro
               raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="Usuário não encontrado"
                     )

            # Gerar um novo token
            exp = datetime.utcnow() + timedelta(minutes=30)  # Novo tempo de expiração
            new_payload = {
                   "sub": username,
                   "exp": exp,
                   "cargo": usuario_no_bd.cargo,
                 }
            new_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)
            print(f"Novo token gerado: {new_token}")  # Log do novo token
            return {"token_de_acesso": new_token, "expiração": exp.isoformat()}

        except JWTError as e:
            print(f"Erro na decodificação do token: {e}")  # Log de erro
            raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Token inválido ou expirado",
        )

    
    

    
        

    