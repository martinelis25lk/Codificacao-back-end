from api.models.usuario_model import UserModel
from api.routers.usuario_router import UsuarioResponse
from fastapi import HTTPException, status

def test_create_user(session):
        # Criação do objeto UserModel
        usuario = UserModel(
            username='dunossaura',
            password='minha_senha',
            cargo='usuario'
        )

        # Adiciona o usuário ao banco e salva as mudanças
        session.add(usuario)
        session.commit()
        

        # Verificações
        assert usuario.username == 'dunossaura'
        assert usuario.password == 'minha_senha'
        assert usuario.cargo == 'usuario'


def test_read_users(client, usuario):
        response = client.get('/usuarios/listar_usuarios')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{
                'id': usuario.id,
                'username': usuario.username,
                'password': usuario.password,
                'cargo': usuario.cargo
        }]

def test_read_users_empty(client, session):
    # Certifique-se de que o banco está limpo
    
    response = client.get('/usuarios/listar_usuarios')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []




def test_read_usuario_com_usuario(client, usuario):
    # Valida e transforma a instância do usuário diretamente no formato esperado pelo modelo
    usuario_schema = UsuarioResponse.model_validate(usuario)
    
    # Requisitar a listagem de usuários
    response = client.get('/usuarios/listar_usuarios')
    
    # Validando o status da resposta e o conteúdo retornado
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [usuario_schema.dict()]


def test_atualiza_usuario(client, usuario, token_fixture):
    response = client.put(
        f'/usuarios/atualizar_usuario/{usuario.id}',
        headers={'Authorization': f'Bearer {token_fixture}'},
        json={
             'username':'teste',
             'password':'teste@',  
             'id': usuario.id,
             'cargo':'usuario'
        },
    )
    response_data = response.json()
    assert response_data['username'] == 'teste'
    assert response_data['id'] == usuario.id
    assert response_data['cargo'] == 'usuario'
    assert 'password' in response_data


    
def test_deletar_usuario(client, usuario, token_fixture):
    response = client.delete(
        f'/usuarios/deletar_usuario/{usuario.id}',
        headers={'Authorization': f'Bearer {token_fixture}'},
          )

    assert response.json() == {'msg': 'usuario deletado'}
 




#testando o endpoint token
def test_get_token(client, usuario):
    response = client.post('/usuarios/token', 
        data = {'username': usuario.username, 
                'password': usuario.senha_limpa},
        )
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token['tipo_de_token'] == 'Bearer'
    assert 'token_de_acesso' in token  
