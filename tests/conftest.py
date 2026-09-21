"""Configuración de las pruebas.

Cada corrida usa una base SQLite temporal y aislada, así que las pruebas
nunca tocan la base real ni dependen de MySQL/PostgreSQL.
"""

import os
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# La URL se define ANTES de importar la app: app/config.py la lee al importarse.
_DB_DIR = tempfile.mkdtemp(prefix="checador-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_DB_DIR, 'tests.db')}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def base_limpia():
    """Deja las tablas vacías antes de cada prueba."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
