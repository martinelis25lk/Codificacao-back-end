from fastapi.testclient import TestClient


from api.shared.database import Base, engine
from api.shared.dependencies import get_db

from api.main import app

client = TestClient(app)





#post=====================================================================

def test_deve_criar_cliente():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    
    novo_cliente = {'cpf': '07399627363', 
                    'nome': 'guilherme eduardo almeida', 
                    'email':'gui.almeida.edu@gmail.com'
                    }
    response = client.post("/clientes/cria_cliente", json=novo_cliente)
    assert response.status_code == 200
    assert response.json()["nome"] == "guilherme eduardo almeida"


def test_cria_cliente_com_cpf_invalido():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    cliente_com_cpf_invalido = {'id': 1, 'nome':'zeca', 'cpf': '123', 'email': 'email@gmail.com'}

    response = client.post("/clientes/cria_cliente",json=cliente_com_cpf_invalido)
    assert response.status_code == 400

    

def test_cria_cliente_com_email_invalido():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    cliente_com_email_invalido = {'id': 1, 'nome':'zeca', 'cpf': '70025509349', 'email': '123'}

    response = client.post('/clientes/cria_cliente', json=cliente_com_email_invalido)

    assert response.status_code == 400


def test_campo_cpf_obrigatorio_ausente():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    
    #tentando criar cliente sem cpf
    response_cpf = client.post('/clientes/cria_cliente', 
                           json={'nome': 'cliente teste', 'email':'test@gmail.com'}
                           )
    assert response_cpf.status_code == 422
    assert 'cpf' in response_cpf.json()['detail'][0]['loc']




def test_testa_campo_email_obrigatorio_ausente():
    #tenta criar cliente sem email
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    response_email = client.post('/clientes/cria_cliente', json={'nome':'guilhermekk', 'cpf':'70025509349'}
                                 )
    assert response_email.status_code == 422
    assert 'email' in response_email.json()['detail'][0]['loc']



def test_testa_campo_nome_obrigatorio_ausente():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    #tenta criar cliente sem nome 

    response_nome = client.post('/clientes/cria_cliente', json={'email':'gui.almeida.edu@gmail.com','cpf':'12345678912'}
                                )
    assert response_nome.status_code == 422


    assert 'nome' in response_nome.json()['detail'][0]['loc']


def test_duplicao_de_cpf():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    #criar um cliente inicial com cpf unico
    response = client.post('/clientes/cria_cliente',
     json={'nome': ' eduardo', 'cpf':'48271506056', 'email':'eduardo@gmail.com'})
    
    assert response.status_code == 200
    assert response.json()['cpf'] == '48271506056'

    #tentar criar outro cliente com o msm cpf
    response = client.post('/clientes/cria_cliente', json={'nome': 'jose','email':'jose@gmail.com','cpf':'48271506056'}
                           )
    assert response.status_code == 400
    assert response.json()['detail'] == 'Cliente com este CPF já está cadastrado' 






#get========================================================================================================



#get com id================================================================================================

def test_buscar_cliente_existente():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post('/clientes/cria_cliente', json={'nome': 'Joao', 'cpf': '12345678901', 'email': 'joao@gmail.com'})

    response = client.get('clientes/pegar_cliente_id/1')

    assert response.status_code == 200
    cliente = response.json()
    
    assert cliente['nome']  == 'Joao'
    assert cliente['cpf']   == '12345678901'
    assert cliente['email'] == 'joao@gmail.com'

def test_buscar_cliente_inexistente():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    response = client.get('/clientes/pegar_cliente_id/99')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Cliente não encontrado'





#put/patch=================================================================================================


def test_atualizar_cliente_valido():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post('/clientes/cria_cliente', json={'nome': 'lucas', 'cpf':'76144332030', 'email':'lucas@gmail.com'})

    response = client.put('/clientes/atualizar_cliente_id/1',
    json={'nome': 'Lucas Silva', 'cpf': '98765432100', 'email': 'lucas.silva@gmail.com'})

    assert response.status_code == 200
    assert response.json()['nome']  == 'Lucas Silva'
    assert response.json()['cpf']   == '98765432100'
    assert response.json()['email'] == 'lucas.silva@gmail.com'


def test_atualizar_cliente_inexistente():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    response = client.put('/clientes/atualizar_cliente_id/99', 
    json={'nome': 'guilherme eduardo', 'cpf':'09313033038', 'email':'guilherme@gmail.com'})


    assert response.status_code == 404
    assert response.json()['detail'] == 'Cliente não encontrado'


def test_atualizar_cliente_parcial():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post('/clientes/cria_cliente', 
        json={'nome': 'Joao', 'cpf': '59311655090', 'email': 'joao@gmail.com'})

    response = client.put('/clientes/atualizar_cliente_id/1',
    json={'nome': 'joao neto', 'cpf': '59311655090', 'email': 'joao@gmail.com'})
    
    assert response.status_code == 200
    cliente = response.json()
    assert cliente['nome']  == 'joao neto'
    assert cliente['cpf']   == '59311655090'     #campo mantido
    assert cliente['email'] == 'joao@gmail.com'  #campo mantido




def test_atualizar_cliente_dados_invalidos():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/clientes/cria_cliente', 
    json={'nome':'paula', 'cpf':'52929814004', 'email': 'paula@gmail.com'})

    response = client.put('clientes/atualizar_cliente_id/1',
        json={'cpf':'invalido'})
    
    assert response.status_code == 422







#delete====================================================================================================

def test_excluir_cliente_valido():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/clientes/cria_cliente', json={
        'nome':'carlos',
        'cpf':'90862951003',
        'email': 'carlos@gmail.com'
    })

    response = client.delete('/clientes/excluir_cliente/1')
    assert response.status_code == 204
    
    #tentar buscar cliente apos exclusao

    response_busca = client.get('/clientes/pegar_cliente_id/1')

    response_duplicada = client.delete('/clientes/excluir_cliente/1')
    assert response_duplicada.status_code == 404
    assert response_duplicada.json()['detail'] == "Cliente não encontrado"








#==========================================================================================================


def test_deve_listar_todos_os_clientes():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post("/clientes/cria_cliente", json={'id': 1, 'cpf': '11111111111', 'nome': 'mel', 'email': 'mel@gmail.com'})
    client.post("/clientes/cria_cliente", json={'id': 2, 'cpf': '22222222222', 'nome': 'string', 'email': 'teste@gmail.com'})
    client.post("/clientes/cria_cliente", json={'id': 3, 'cpf': '33333333333', 'nome': 'crismel mota', 'email': 'mel@gmail.comkkkkkk'})

    
    response = client.get("/clientes/listar_com_paginacao")
    

    
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()==[
        {'id': 1, 'cpf': '11111111111', 'nome': 'mel', 'email': 'mel@gmail.com'},
         {'id': 2, 'cpf': '22222222222', 'nome': 'string', 'email': 'teste@gmail.com'},
         {'id': 3, 'cpf': '33333333333', 'nome': 'crismel mota', 'email': 'mel@gmail.comkkkkkk'}
    ]


def test_deve_retornar_lista_vazia_ao_listar_sem_clientes():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    response = client.get("/clientes/listar_com_paginacao")

    assert response.status_code == 200
    assert response.json() == []


def test_listar_com_paginacao():
    #testando a funcionalidade de paginacao

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    
   
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente0','cpf': '25646378095', 'email': 'mel@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente1','cpf': '49540317029', 'email': 'fuilherme@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente2','cpf': '08437626080', 'email': '222@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente3','cpf': '05268361058', 'email': 'eduardo@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente4','cpf': '25941676069', 'email': 'almeida@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente5','cpf': '05387460092', 'email': 'martinelis@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente6','cpf': '65393076088', 'email': 'gris@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente7','cpf': '08878330043', 'email': 'joao@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente8','cpf': '40679033084', 'email': 'carlos@gmail.com'})
    client.post("/clientes/cria_cliente", json={ 'nome': 'cliente9','cpf': '55155124050', 'email': 'marta@gmail.com'})
    
    #chamar a pagina 1 com limite de 5 clientes por pagina
    response = client.get('/clientes/listar_com_paginacao?p=1&page_size=5')


  
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]['nome'] == 'cliente0' #verificcar o primeiro cliente


def test_listar_com_filtro_por_nome():
    #testar se o filtrop por nome ou email funciona

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post('/clientes/cria_cliente', json={'nome': 'Alice', 'cpf': '11111111111', 'email': 'alice@gmail.com'})
    client.post('/clientes/cria_cliente', json={'nome': 'Bob', 'cpf': '22222222222', 'email': 'bob@gmail.com'})

    response = client.get('/clientes/listar_com_paginacao?nome=Alice')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {'id': 1, 'nome': 'Alice', 'cpf': '11111111111', 'email':'alice@gmail.com'}

    



