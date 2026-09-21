"""Pruebas de la API Reloj Checador.

Cubren empleados, checadas y reportes. No tocan el checador físico ni
requieren base de datos externa: todo corre sobre SQLite temporal.
"""

from datetime import datetime, timedelta

from app.database.database import SessionLocal
from app.models.check_in import CheckIn

EMPLEADOS = "/api/v1/employees/"
CHECADAS = "/api/v1/check-ins/"


def crear_empleado(
    client, employee_id="EMP-001", email="ana@example.com", department="Producción", name="Ana Paula"
):
    respuesta = client.post(
        EMPLEADOS,
        json={
            "name": name,
            "email": email,
            "employee_id": employee_id,
            "department": department,
            "position": "Analista",
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def sembrar_jornada(employee_id: int, inicio: datetime, horas: float = 2.5):
    """Inserta una checada ya cerrada con horario conocido."""
    db = SessionLocal()
    try:
        db.add(
            CheckIn(
                employee_id=employee_id,
                check_in_time=inicio,
                check_out_time=inicio + timedelta(hours=horas),
            )
        )
        db.commit()
    finally:
        db.close()


# --- Servicio vivo ---------------------------------------------------------


def test_raiz_y_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json() == {"status": "healthy"}


def test_openapi_se_genera(client):
    respuesta = client.get("/openapi.json")
    assert respuesta.status_code == 200
    assert "/api/v1/employees/" in respuesta.json()["paths"]


# --- Empleados -------------------------------------------------------------


def test_crear_empleado(client):
    empleado = crear_empleado(client)
    assert empleado["id"] > 0
    assert empleado["email"] == "ana@example.com"
    assert empleado["is_active"] is True


def test_email_duplicado_se_rechaza(client):
    crear_empleado(client)
    respuesta = client.post(
        EMPLEADOS,
        json={"name": "Otra", "email": "ana@example.com", "employee_id": "EMP-002"},
    )
    assert respuesta.status_code == 400


def test_employee_id_duplicado_se_rechaza(client):
    crear_empleado(client)
    respuesta = client.post(
        EMPLEADOS,
        json={"name": "Otra", "email": "otra@example.com", "employee_id": "EMP-001"},
    )
    assert respuesta.status_code == 400


def test_email_invalido_se_rechaza(client):
    respuesta = client.post(
        EMPLEADOS,
        json={"name": "Mala", "email": "no-es-un-correo", "employee_id": "EMP-003"},
    )
    assert respuesta.status_code == 422


def test_listar_y_obtener_empleado(client):
    creado = crear_empleado(client)
    listado = client.get(EMPLEADOS)
    assert listado.status_code == 200
    assert [e["id"] for e in listado.json()] == [creado["id"]]

    detalle = client.get(f"{EMPLEADOS}{creado['id']}")
    assert detalle.status_code == 200
    assert detalle.json()["name"] == "Ana Paula"


def test_empleado_inexistente_devuelve_404(client):
    assert client.get(f"{EMPLEADOS}9999").status_code == 404


def test_actualizar_empleado(client):
    creado = crear_empleado(client)
    respuesta = client.put(f"{EMPLEADOS}{creado['id']}", json={"position": "Coordinadora"})
    assert respuesta.status_code == 200
    assert respuesta.json()["position"] == "Coordinadora"
    assert respuesta.json()["name"] == "Ana Paula"


def test_desactivar_empleado(client):
    creado = crear_empleado(client)
    assert client.delete(f"{EMPLEADOS}{creado['id']}").status_code == 204
    assert client.get(f"{EMPLEADOS}{creado['id']}").json()["is_active"] is False


# --- Checadas --------------------------------------------------------------


def test_flujo_completo_de_checada(client):
    empleado = crear_empleado(client)

    entrada = client.post(f"{CHECADAS}check-in", json={"employee_id": empleado["id"]})
    assert entrada.status_code == 201, entrada.text
    registro = entrada.json()
    assert registro["check_out_time"] is None

    repetida = client.post(f"{CHECADAS}check-in", json={"employee_id": empleado["id"]})
    assert repetida.status_code == 400

    salida = client.post(f"{CHECADAS}{registro['id']}/check-out", json={"notes": "Fin de turno"})
    assert salida.status_code == 200, salida.text
    assert salida.json()["check_out_time"] is not None
    assert salida.json()["notes"] == "Fin de turno"

    salida_repetida = client.post(f"{CHECADAS}{registro['id']}/check-out", json={})
    assert salida_repetida.status_code == 400


def test_checada_de_empleado_inexistente(client):
    assert client.post(f"{CHECADAS}check-in", json={"employee_id": 9999}).status_code == 404


def test_checada_de_empleado_inactivo(client):
    empleado = crear_empleado(client)
    client.delete(f"{EMPLEADOS}{empleado['id']}")
    respuesta = client.post(f"{CHECADAS}check-in", json={"employee_id": empleado["id"]})
    assert respuesta.status_code == 400


def test_listar_checadas_filtra_por_empleado(client):
    ana = crear_empleado(client, employee_id="EMP-001", email="ana@example.com")
    luis = crear_empleado(client, employee_id="EMP-002", email="luis@example.com")

    assert client.post(f"{CHECADAS}check-in", json={"employee_id": ana["id"]}).status_code == 201
    assert client.post(f"{CHECADAS}check-in", json={"employee_id": luis["id"]}).status_code == 201

    todas = client.get(CHECADAS)
    assert todas.status_code == 200
    assert len(todas.json()) == 2

    solo_ana = client.get(CHECADAS, params={"employee_id": ana["id"]})
    assert [r["employee_id"] for r in solo_ana.json()] == [ana["id"]]

    assert client.get(f"{CHECADAS}9999").status_code == 404


# --- Reportes --------------------------------------------------------------


def test_reporte_diario_y_mensual(client):
    empleado = crear_empleado(client)
    hoy = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    sembrar_jornada(empleado["id"], hoy, horas=2.5)

    diario = client.get(
        f"/api/v1/reports/employee/{empleado['id']}/daily",
        params={"date": hoy.date().isoformat()},
    )
    assert diario.status_code == 200, diario.text
    assert diario.json()["employee_name"] == "Ana Paula"
    assert diario.json()["total_hours"] == 2.5

    mensual = client.get(
        f"/api/v1/reports/employee/{empleado['id']}/monthly",
        params={"year": hoy.year, "month": hoy.month},
    )
    assert mensual.status_code == 200, mensual.text
    assert mensual.json()["total_check_ins"] == 1
    assert mensual.json()["total_hours"] == 2.5


def test_reporte_de_departamento(client):
    ana = crear_empleado(client, employee_id="EMP-001", email="ana@example.com")
    crear_empleado(
        client,
        employee_id="EMP-002",
        email="luis@example.com",
        department="Producción",
        name="Luis Ramírez",
    )
    hoy = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    sembrar_jornada(ana["id"], hoy, horas=4)

    respuesta = client.get(
        "/api/v1/reports/department/Producción",
        params={"date": hoy.date().isoformat()},
    )
    assert respuesta.status_code == 200, respuesta.text
    por_empleado = {e["employee_name"]: e for e in respuesta.json()["employees"]}
    assert len(por_empleado) == 2
    assert por_empleado["Ana Paula"]["total_hours"] == 4.0
    assert por_empleado["Ana Paula"]["check_count"] == 1
    assert por_empleado["Luis Ramírez"]["total_hours"] == 0.0
    assert por_empleado["Luis Ramírez"]["check_count"] == 0

    assert client.get("/api/v1/reports/department/Inexistente").status_code == 404


def test_reporte_de_empleado_inexistente(client):
    assert client.get("/api/v1/reports/employee/9999/daily").status_code == 404
    assert client.get("/api/v1/reports/employee/9999/monthly").status_code == 404
