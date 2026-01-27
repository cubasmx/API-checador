from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import employees, check_ins, reports

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Reloj Checador",
    description="API para gestionar entrada y salida de empleados",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(employees.router)
app.include_router(check_ins.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API Reloj Checador",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
