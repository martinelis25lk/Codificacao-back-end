from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from auth.auth_usuario import UserUseCases
from auth.schemas import User
from fastapi.security import OAuth2PasswordRequestForm

#from app.depends import get_db_session, token_verifier

router = APIRouter(prefix='/usuario')


@router.post('/register')
def user_register(
    user: User,
    db_session: Session = Depends(get_db),
):
    uc = UserUseCases(db_session=db_session)
    uc.usuario_register(user=user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED,
    )



@router.post('/login')
def user_register(login_request_form : OAuth2PasswordRequestForm= Depends()
                  ,db_session: Session = Depends(get_db)):
    
    uc = UserUseCases(db_session=db_session)
    user = User(
        username=login_request_form.username,
        password=login_request_form.password
    )

    auth_data = uc.usuario_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )