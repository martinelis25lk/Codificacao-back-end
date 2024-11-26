from shared.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from auth.auth_usuario import UserUseCases
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from auth.auth_usuario import SECRET_KEY, ALGORITHM

from models.usuario_model import UserModel

#oauth_scheme = OAuth2PasswordBearer(tokenUrl='/usuario/login')


def get_db():
    db = SessionLocal()
    try:
        yield db   # Retorna a sessão enquanto a rota estiver em execução
    finally:
        db.close()

def obtem_usuario_atual(
        token : str = Depends(OAuth2PasswordBearer(tokenUrl='/usuario/login')),
        db_session: Session = Depends(get_db)
):
    try:
        #decodifica o token JWT
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        cargo    = payload.get('cargo')

        if username is None or cargo is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='credenciais invalidas ou expiradas'
            ) 
        
        #verifica se o usuario existe no banco 

        usuario_no_bd = db_session.query(UserModel).filter_by(username=username).first()

        if usuario_no_bd is None:
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='usuario nao encontrado'
            )
        
        return {"username": username, "cargo": cargo}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="teste: credenciais invalidas ou expiradas"
        )


    


def admin_validacao(usuaio_atual: dict = Depends(obtem_usuario_atual)):
    if usuaio_atual['cargo'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ação restrita a administradores"
        )
    
    return usuaio_atual


def usuario_validacao(usuario_atual: dict = Depends(obtem_usuario_atual)):
    #todos os usuarios autenticados podem acessar, sem restrição de cargo
    return usuario_atual