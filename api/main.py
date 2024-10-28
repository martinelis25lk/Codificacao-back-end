from fastapi import FastAPI
import uvicorn
from routers.clientes_routers import router as clientes_router
from routers.usuario_router import user_router as usuario_router 
from shared.database import engine, Base
from models.clientes_models import ClienteModel
from auth.auth_usuario import UserModel

#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)



app = FastAPI()




@app.get("/")
def ola_mundo_do_fastapi():
    return {"hello":"worlddddd"}






app.include_router(clientes_router)
app.include_router(usuario_router)


if __name__== "__main__":
   uvicorn.run(app, host="localhost",port=8080)


   #caminho de instalação das dependencias
   #(.venv) PS C:\Users\guial\projetos python\TESTE> 