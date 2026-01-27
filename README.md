# API Reloj Checador

Una API moderna construida con FastAPI para gestionar entrada y salida de empleados (sistema de asistencia).

## Características

- ✅ Gestión de empleados
- ✅ Registro de entrada/salida
- ✅ Reportes diarios y mensuales
- ✅ Reportes por departamento
- ✅ Base de datos con SQLAlchemy
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática con Swagger UI

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clona o descarga el proyecto
2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Copia el archivo `.env.example` a `.env` y configura tus variables:
```bash
cp .env.example .env
```

## Ejecutar la aplicación

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### Documentación interactiva
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estructura del proyecto

```
API-checador/
├── app/
│   ├── models/           # Modelos de base de datos
│   │   ├── employee.py   # Modelo de empleado
│   │   └── check_in.py   # Modelo de entrada/salida
│   ├── routes/           # Rutas/endpoints
│   │   ├── employees.py  # Endpoints de empleados
│   │   ├── check_ins.py  # Endpoints de entrada/salida
│   │   └── reports.py    # Endpoints de reportes
│   ├── schemas/          # Esquemas Pydantic
│   │   ├── employee.py   # Schema de empleado
│   │   └── check_in.py   # Schema de entrada/salida
│   ├── database/         # Configuración de base de datos
│   │   └── database.py   # Conexión y sesión
│   ├── config.py         # Configuración general
│   └── main.py           # Aplicación principal
├── requirements.txt      # Dependencias
├── .env.example         # Variables de entorno (ejemplo)
└── README.md            # Este archivo
```

## Endpoints principales

### Empleados
- `POST /api/v1/employees/` - Crear empleado
- `GET /api/v1/employees/` - Listar empleados
- `GET /api/v1/employees/{id}` - Obtener empleado
- `PUT /api/v1/employees/{id}` - Actualizar empleado
- `DELETE /api/v1/employees/{id}` - Desactivar empleado

### Entrada/Salida
- `POST /api/v1/check-ins/check-in` - Registrar entrada
- `POST /api/v1/check-ins/{id}/check-out` - Registrar salida
- `GET /api/v1/check-ins/` - Listar registros
- `GET /api/v1/check-ins/{id}` - Obtener registro

### Reportes
- `GET /api/v1/reports/employee/{id}/daily` - Reporte diario
- `GET /api/v1/reports/employee/{id}/monthly` - Reporte mensual
- `GET /api/v1/reports/department/{name}` - Reporte por departamento

## Base de datos

Por defecto, el proyecto usa SQLite para desarrollo. Para usar PostgreSQL:

1. Actualiza la variable `DATABASE_URL` en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/checador_db
```

2. Instala el driver de PostgreSQL:
```bash
pip install psycopg2-binary
```

## Desarrollo futuro

- [ ] Autenticación y autorización
- [ ] Manejo de vacaciones y permisos
- [ ] Notificaciones
- [ ] Exportación de reportes (PDF, Excel)
- [ ] Dashboard web
- [ ] Aplicación móvil

## Licencia

MIT
