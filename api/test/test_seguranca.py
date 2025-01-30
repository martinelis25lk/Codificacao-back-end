from api.autenticacao.funcoes_auxiliares_token import criar_token_de_acesso, SECRET_KEY, ALGORITHM
from jwt import decode
from fastapi import HTTPException, status




def test_jwt():
    data = {'sub':'test@test.com'}
    token = criar_token_de_acesso(data)

    result  = decode(token, SECRET_KEY, [ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']



def test_jwt_token_invalido(client):
    response = client.delete(
         '/usuarios/deletar_usuario/1', headers={'Authorization' : 'Bearer  token-inválido'.encode('utf-8')}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'could not validate credentials'}