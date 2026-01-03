"""
Configuración de fixtures para pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.task import Task

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Fixture que proporciona una sesión de base de datos limpia para cada test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Fixture que proporciona un cliente de prueba de FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Fixture que crea un usuario de prueba"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_token(client, test_user):
    """Fixture que proporciona un token JWT válido"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(test_user_token):
    """Fixture que proporciona headers de autenticación"""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def test_task(db_session, test_user):
    """Fixture que crea una tarea de prueba"""
    from app.models.task import TaskStatus
    task = Task(
        title="Tarea de prueba",
        description="Descripción de prueba",
        status=TaskStatus.PENDING
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task
