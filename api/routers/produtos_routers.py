from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from typing import List
from decimal import Decimal
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from models.produtos_models import ProdutoModel
from typing import List, Optional
from datetime import datetime





#categoria, preço, disponibilidade, descricao, valor de venda, codigo de barras, seção, estoque inicial, data de validade, imagens


router = APIRouter(prefix="/produtos")



class ProdutoCategoriaTipoEnum(str, Enum):
    MEDICAMENTO = "medicamento"
    ALIMENTO = "alimento"
    OUTROS = "outros"

# Modelo Pydantic para resposta de produto
class Produto_Response(BaseModel):
    codigo: int
    descricao: str
    preco: Decimal
    data_de_validade: datetime
    categoria: ProdutoCategoriaTipoEnum
    disponibilidade: bool
    codigo_de_barras: str
    secao: str
    estoque_inicial: int
    imagem: str



class Produto_Request(BaseModel):
    descricao        : str
    preco            : Decimal
    data_de_validade : datetime   
    categoria        : ProdutoCategoriaTipoEnum
    disponibilidade  : bool
    codigo_de_barras : str
    secao            : str
    estoque_inicial  : int
    imagem           : str



@router.post("/produtos", response_model=Produto_Response)
def ciar_produto(produto_request : Produto_Request, 
                 db:Session = Depends(get_db))-> Produto_Response:
        produto_a_ser_criado = ProdutoModel(
                **produto_request.model_dump()
                )
        db.add(produto_a_ser_criado)
        db.commit()
        db.refresh(produto_a_ser_criado)

        return produto_a_ser_criado

#def criar_conta(conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
#                 db : Session = Depends(get_db))-> ContaPagarReceberResponse:
    
#    _valida_fornecedor(conta_a_pagar_e_receber_request.fornecedor_cliente_id, db)
#    contas_a_pagar_e_receber = ContaPagarReceber(
#        **conta_a_pagar_e_receber_request.dict()
#    )

#    db.add(contas_a_pagar_e_receber)
#    db.commit()
#    db.refresh(contas_a_pagar_e_receber)

#    return contas_a_pagar_e_receber



@router.get("/produto/{id_do_produto}", response_model=Produto_Response)
def pegar_produto_por_id(id_do_produto: int, db: Session = Depends(get_db))-> Produto_Response:
    return buscar_produto_por_id(id_do_produto, db)




@router.get("/produtos", response_model=list[Produto_Response])
def listar_produtos(db:Session= Depends(get_db))-> list[Produto_Response]:
    produtos = db.query(ProdutoModel).all()

    return produtos



@router.delete("produto/{id_do_produto}")
def excluir_produto(id_do_produto: int, db:Session= Depends(get_db))-> None:
    produto_a_ser_excluido = db.query(ProdutoModel).get(id_do_produto)

    db.delete(produto_a_ser_excluido)
    db.commit()



@router.put("/produtos/{id_do_produto}", response_model= Produto_Response)
def atualizar_produto(id_do_produto: int, produto_request : Produto_Request,
                       db:Session = Depends(get_db))-> Produto_Response:
    produto_a_ser_alterado = buscar_produto_por_id(id_do_produto, db)
    produto_a_ser_alterado.descricao        = produto_request.descricao
    produto_a_ser_alterado.data_de_validade = produto_request.data_de_validade
    produto_a_ser_alterado.codigo_de_barras = produto_request.codigo_de_barras
    produto_a_ser_alterado.categoria        =  produto_request.categoria
    produto_a_ser_alterado.disponibilidade  = produto_request.disponibilidade 
    produto_a_ser_alterado.estoque_inicial  = produto_request.estoque_inicial
    produto_a_ser_alterado.imagem           = produto_request.imagem
    produto_a_ser_alterado.secao            = produto_request.secao
    produto_a_ser_alterado.preco            = produto_request.preco

    
    db.add(produto_a_ser_alterado)
    db.commit()
    db.refresh(produto_a_ser_alterado)

    return produto_a_ser_alterado
     

      



def buscar_produto_por_id(id_do_produto: int, db: Session) -> Produto_Response:
    produto_a_ser_retornado = db.query(ProdutoModel).get(id_do_produto)
    if produto_a_ser_retornado is None:
        raise("este produto não existe")
    

    return produto_a_ser_retornado





