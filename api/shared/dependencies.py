from api.shared.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from api.models.usuario_model import UserModel




def get_db():
    db = SessionLocal()
    try:
        yield db   # Retorna a sessão enquanto a rota estiver em execução
    finally:
        db.close()


    



