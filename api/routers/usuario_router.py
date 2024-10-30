from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from auth.auth_usuario import UserUseCases
from auth.schemas import User





#from app.depends import get_db_session, token_verifier


router = APIRouter(prefix='/user')


@router.post('/register')
def user_register(
    user: User,
    db_session: Session = Depends(get_db),
):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED,
        
    )



