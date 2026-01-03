"""
Tests para servicios (capa de negocio)
"""
import pytest
from app.services import task_service, auth_service
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.security import get_password_hash


class TestTaskService:
    """Tests para el servicio de tareas"""
    
    def test_create_task(self, db_session):
        """Test: Crear tarea a través del servicio"""
        task_data = TaskCreate(
            title="Tarea de servicio",
            description="Descripción de prueba",
            status="pending"
        )
        
        task = task_service.create_task(db_session, obj_in=task_data)
        
        assert task.id is not None
        assert task.title == task_data.title
        assert task.description == task_data.description
        assert task.status == TaskStatus.PENDING
        assert task.created_at is not None
    
    def test_get_task(self, db_session, test_task):
        """Test: Obtener tarea por ID"""
        task = task_service.get_task(db_session, task_id=test_task.id)
        
        assert task is not None
        assert task.id == test_task.id
        assert task.title == test_task.title
    
    def test_get_task_not_found(self, db_session):
        """Test: Obtener tarea inexistente retorna None"""
        task = task_service.get_task(db_session, task_id=99999)
        
        assert task is None
    
    def test_get_tasks_pagination(self, db_session):
        """Test: Obtener tareas con paginación"""
        # Crear 5 tareas
        for i in range(5):
            task = Task(
                title=f"Tarea {i}",
                status=TaskStatus.PENDING
            )
            db_session.add(task)
        db_session.commit()
        
        # Obtener primeras 3
        tasks = task_service.get_tasks(db_session, skip=0, limit=3)
        assert len(tasks) == 3
        
        # Obtener siguientes 2
        tasks = task_service.get_tasks(db_session, skip=3, limit=3)
        assert len(tasks) == 2
    
    def test_update_task(self, db_session, test_task):
        """Test: Actualizar tarea"""
        update_data = TaskUpdate(
            title="Título actualizado",
            status="in_progress"
        )
        
        updated_task = task_service.update_task(
            db_session,
            db_obj=test_task,
            obj_in=update_data
        )
        
        assert updated_task.title == "Título actualizado"
        assert updated_task.status == TaskStatus.IN_PROGRESS
    
    def test_update_task_partial(self, db_session, test_task):
        """Test: Actualización parcial mantiene campos no actualizados"""
        original_title = test_task.title
        update_data = TaskUpdate(status="completed")
        
        updated_task = task_service.update_task(
            db_session,
            db_obj=test_task,
            obj_in=update_data
        )
        
        assert updated_task.title == original_title
        assert updated_task.status == TaskStatus.COMPLETED
    
    def test_delete_task(self, db_session, test_task):
        """Test: Eliminar tarea"""
        task_id = test_task.id
        
        task_service.delete_task(db_session, task_id=task_id)
        
        # Verificar que fue eliminada
        task = task_service.get_task(db_session, task_id=task_id)
        assert task is None


class TestAuthService:
    """Tests para el servicio de autenticación"""
    
    def test_authenticate_user_success(self, db_session, test_user):
        """Test: Autenticar usuario con credenciales correctas"""
        user = auth_service.authenticate(
            db_session,
            email="test@example.com",
            password="testpass123"
        )
        
        assert user is not None
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_authenticate_user_wrong_password(self, db_session, test_user):
        """Test: Autenticación falla con contraseña incorrecta"""
        user = auth_service.authenticate(
            db_session,
            email="test@example.com",
            password="wrongpassword"
        )
        
        assert user is None
    
    def test_authenticate_user_not_found(self, db_session):
        """Test: Autenticación falla con usuario inexistente"""
        user = auth_service.authenticate(
            db_session,
            email="noexiste@example.com",
            password="password123"
        )
        
        assert user is None
    
    def test_get_user_by_email(self, db_session, test_user):
        """Test: Obtener usuario por email"""
        user = auth_service.get_user_by_email(
            db_session,
            email="test@example.com"
        )
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_get_user_by_email_not_found(self, db_session):
        """Test: Obtener usuario inexistente retorna None"""
        user = auth_service.get_user_by_email(
            db_session,
            email="noexiste@example.com"
        )
        
        assert user is None
