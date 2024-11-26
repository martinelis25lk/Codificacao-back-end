from fastapi import APIRouter, Depends, status,  HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from auth.auth_usuario import UserUseCases
from auth.schemas import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from routers.clientes_routers import router

from shared.dependencies import usuario_validacao, admin_validacao

from auth.schemas import RefreshTokenSchema

router = APIRouter(prefix='/usuario')
#test_routers = APIRouter(prefix='/teste', dependencies=[Depends(verificador_de_token)])





@router.post('/registrar',dependencies=[Depends(admin_validacao)])
def registrar_usuario( 
    user_dados: User, 
    db_session : Session = Depends(get_db),
    
):
    
    uc = UserUseCases(db_session=db_session)
    uc.registrar_usuario(user=user_dados)
    return JSONResponse(
        content={'msg': 'sucess'},
        status_code=status.HTTP_201_CREATED,
    )
    
    




@router.post('/login')
def login_de_usuario(
    request_form_user : OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    
    uc = UserUseCases(db_session=db_session)
    user = User( 
        username=request_form_user.username,
        password=request_form_user.password,
    )

    auth_data = uc.usuario_login(user=user)


    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )



@router.post('/refresh-token')
def refresh_token(
    token_data: RefreshTokenSchema,  # O token será recebido no corpo da requisição
    db_session: Session = Depends(get_db)
):
    print(f"Recebendo requisição de refresh-token com token: {token_data.token}")  # Log inicial

    uc = UserUseCases(db_session=db_session)
    new_token = uc.refresh_user_token(token=token_data.token)

    print(f"Novo token gerado com sucesso: {new_token}")  # Log do novo token gerado
    return JSONResponse(
        content=new_token,  # `new_token` já é um dicionário
        status_code=status.HTTP_200_OK
    )


