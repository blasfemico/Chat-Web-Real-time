from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import auth_router
from websockets.chat import chat_router
from database import init_db

app = FastAPI()

# Configuración CORS (para permitir acceso desde el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes de origen (en producción es mejor limitarlo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos al inicio de la aplicación
@app.life_span("startup")
async def startup_event():
    await init_db() 

# Ruta básica para verificar que la API está funcionando
@app.get("/")
def read_root():
    return {"message": "API is up and running"}

# Incluir rutas de otros módulos (autenticación, chat)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
