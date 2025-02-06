from fastapi import FastAPI, Depends
import uvicorn
from api.routers.clientes_routers import router as clientes_router
from api.routers.produtos_routers import router as produto_router
from api.routers.pedidos_routers import router as pedido_router
from api.routers.usuario_router import router as usuario_router
from api.shared.database import engine, Base



app = FastAPI()





app.include_router(produto_router)
app.include_router(clientes_router)
app.include_router(pedido_router)
app.include_router(usuario_router)



if __name__== "__main__":
   uvicorn.run(app, host="localhost",port=8080)


 
