from shared.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from auth.auth_usuario import UserUseCases
from fastapi import Depends

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/usuario/login')


def get_db():
    db = SessionLocal()
    try:
        yield db   # Retorna a sessão enquanto a rota estiver em execução
    finally:
        db.close()


def verificador_de_token(
        db_session : Session = Depends(get_db),
        token = Depends(oauth_scheme)
):
    uc = UserUseCases(db_session=db_session)
    uc.verifica_token(token_de_acesso=token)
    