from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import (cliente_controller, membresia_controller,
                         asistencia_controller, producto_controller, reporte_controller,
                         registro_cliente_controller, auth_controller)

app = FastAPI(
    title="API Gimnasio",
    description="API REST para gestión completa de gimnasio",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_controller.router)
app.include_router(cliente_controller.router)
app.include_router(membresia_controller.router)
app.include_router(asistencia_controller.router)
app.include_router(producto_controller.router)
app.include_router(reporte_controller.router)
app.include_router(registro_cliente_controller.router)


@app.get("/")
def root():
    return {
        "message": "API Gimnasio - Sistema de Gestión",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
