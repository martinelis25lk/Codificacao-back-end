from fastapi import FastAPI, Depends
import uvicorn
from api.routers.clientes_routers import router as clientes_router

from api.routers.produtos_routers import router as produto_router
from api.routers.pedidos_routers import router as pedido_router
#from routers.usuario_router import test_routers as test_routers
from api.shared.database import engine, Base
from api.models.clientes_models import ClienteModel
from api.models import usuario_model
from api.models.produtos_models import ProdutoModel
from api.models.pedidos_models import PedidoModel


#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)






#app = FastAPI()

app = FastAPI()


@app.get("/")
def ola_mundo_do_fastapi():
    return {"ok":"está funcionando"}





app.include_router(produto_router)
app.include_router(clientes_router)

app.include_router(pedido_router)
#app.include_router(test_routers)


if __name__== "__main__":
   uvicorn.run(app, host="localhost",port=8080)


   #caminho de instalação das dependencias
   #(.venv) PS C:\Users\guial\projetos python\TESTE> 


