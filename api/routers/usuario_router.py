from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from auth.auth_usuario import UserUseCases
from auth.schemas import User
from fastapi.security import OAuth2PasswordRequestForm
from shared.dependencies import verificador_de_token

#from app.depends import get_db_session, token_verifier

router = APIRouter(prefix='/usuario')
test_routers = APIRouter(prefix='/test', dependencies=[Depends(verificador_de_token)])


@router.post('/register')
def user_register( user: User, db_session: Session = Depends(get_db)):
    uc = UserUseCases(db_session=db_session)
    uc.usuario_register(user=user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED,
    )



@router.post('/login')
def user_login(request_form_user : OAuth2PasswordRequestForm= Depends()
                  ,db_session: Session = Depends(get_db),
                  ):
    
    uc = UserUseCases(db_session=db_session)
    user = User(
        username=request_form_user.username,
        password=request_form_user.password
    )

    auth_data = uc.usuario_login(user=user)


    return {
        "access_token": auth_data["token_de_acesso"],
        "token_type": "bearer"
    }

@test_routers.get("/teste")
def teste_usuario_verificacao():
    return "it works!"