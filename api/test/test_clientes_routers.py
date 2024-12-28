from fastapi.testclient import TestClient


from api.shared.database import Base, engine
from api.shared.dependencies import get_db

from api.main import app

client = TestClient(app)





#post====

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






#get====



#get com id====


#put/patch====


#delete=======


def test_deve_listar_clientes():

    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    client.post("/clientes/cria_cliente", json={'id': 1, 'cpf': '11111111111', 'nome': 'mel', 'email': 'mel@gmail.com'})
    client.post("/clientes/cria_cliente", json={'id': 2, 'cpf': '22222222222', 'nome': 'string', 'email': 'teste@gmail.com'})
    client.post("/clientes/cria_cliente", json={'id': 3, 'cpf': '33333333333', 'nome': 'crismel mota', 'email': 'mel@gmail.comkkkkkk'})

    
    response = client.get("/clientes/paginacao")
    

    
    assert response.status_code == 200
    assert response.json()==[
        {'id': 1, 'cpf': '11111111111', 'nome': 'mel', 'email': 'mel@gmail.com'},
         {'id': 2, 'cpf': '22222222222', 'nome': 'string', 'email': 'teste@gmail.com'},
         {'id': 3, 'cpf': '33333333333', 'nome': 'crismel mota', 'email': 'mel@gmail.comkkkkkk'}
    ]



