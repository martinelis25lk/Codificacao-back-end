import pytest
from sqlalchemy import create_engine
from api.models.usuario_model import Base
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from api.models.usuario_model import UserModel
from fastapi.testclient import TestClient
from api.shared.database import get_session
from api.autenticacao.funcoes_auxiliares_token import obtem_senha_hash
from api.main import app


@pytest.fixture()
def client(session):

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    
    app.dependency_overrides.clear()

    


@pytest.fixture()
def session():
    engine_test = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        echo=True,
        poolclass=StaticPool)
    
    Base.metadata.create_all(engine_test)

    

    with Session(engine_test) as session:
        yield session

    Base.metadata.drop_all(engine_test) 



@pytest.fixture()
def usuario(session):
    pwd = 'teste@'
    usuario = UserModel(
        username='teste', 
        password= obtem_senha_hash(pwd),
        cargo = 'usuario'
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    usuario.senha_limpa = pwd # monkey patch

    return usuario


@pytest.fixture()
def token_fixture(client, usuario):
    response = client.post(
        '/usuarios/token', data = {'username': usuario.username,'password': usuario.senha_limpa},
    )

    return response.json()['token_de_acesso']