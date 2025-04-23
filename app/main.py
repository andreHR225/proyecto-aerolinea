from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.crud import reserva  
from app.crud import pasajeros
from app.crud import cancelacion
from app.crud import vuelos
from app.crud import tarjetas
from app.crud import clientes
from app.crud import metricas


app = FastAPI()
app.include_router(reserva.router)
app.include_router(pasajeros.router)
app.include_router(clientes.router)
app.include_router(vuelos.router)
app.include_router(tarjetas.router)
app.include_router(cancelacion.router)
app.include_router(metricas.router)
# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos HTML y estáticos
app.mount("/", StaticFiles(directory="frontends", html=True), name="static")

# Incluir rutas API
app.include_router(reserva.router)
