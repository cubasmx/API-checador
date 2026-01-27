<!-- Workspace-specific custom instructions for Copilot -->

## API Reloj Checador - Instrucciones del Proyecto

Este proyecto es una API FastAPI para un sistema de control de asistencia de empleados (reloj checador).

### Estructura del Proyecto
- **app/models** - Modelos de base de datos (Employee, CheckIn)
- **app/routes** - Endpoints de la API (employees, check_ins, reports)
- **app/schemas** - Esquemas Pydantic para validación
- **app/database** - Configuración de base de datos con SQLAlchemy
- **requirements.txt** - Dependencias del proyecto

### Tecnologías
- FastAPI (framework web)
- SQLAlchemy (ORM)
- Pydantic (validación)
- SQLite/PostgreSQL (base de datos)
- Uvicorn (servidor ASGI)

### Comandos útiles
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m uvicorn app.main:app --reload

# Ver documentación
http://localhost:8000/docs
```

### Características implementadas
- Gestión de empleados CRUD
- Registro de entrada/salida
- Cálculo de horas trabajadas
- Reportes diarios y mensuales
- Reportes por departamento
- Documentación automática con Swagger UI
