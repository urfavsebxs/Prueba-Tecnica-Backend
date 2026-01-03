"""
Tests para endpoints de tareas
"""
import pytest
from fastapi import status


class TestTaskEndpoints:
    """Suite de pruebas para endpoints de tareas"""
    
    def test_create_task_success(self, client, auth_headers):
        """Test: Crear tarea exitosamente"""
        task_data = {
            "title": "Nueva tarea",
            "description": "Descripción de la tarea",
            "status": "pending"
        }
        
        response = client.post(
            "/api/v1/tasks",
            json=task_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_without_description(self, client, auth_headers):
        """Test: Crear tarea sin descripción (campo opcional)"""
        task_data = {
            "title": "Tarea sin descripción",
            "status": "pending"
        }
        
        response = client.post(
            "/api/v1/tasks",
            json=task_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] is None
    
    def test_create_task_invalid_title(self, client, auth_headers):
        """Test: Crear tarea con título vacío falla"""
        task_data = {
            "title": "",
            "description": "Descripción",
            "status": "pending"
        }
        
        response = client.post(
            "/api/v1/tasks",
            json=task_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_invalid_status(self, client, auth_headers):
        """Test: Crear tarea con status inválido falla"""
        task_data = {
            "title": "Tarea",
            "status": "invalid_status"
        }
        
        response = client.post(
            "/api/v1/tasks",
            json=task_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_tasks_list(self, client, auth_headers, test_task):
        """Test: Obtener lista de tareas"""
        response = client.get("/api/v1/tasks", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_tasks_pagination(self, client, auth_headers, db_session):
        """Test: Paginación de tareas"""
        # Crear múltiples tareas
        from app.models.task import Task, TaskStatus
        for i in range(15):
            task = Task(
                title=f"Tarea {i}",
                description=f"Descripción {i}",
                status=TaskStatus.PENDING
            )
            db_session.add(task)
        db_session.commit()
        
        # Obtener primera página
        response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 10
        
        # Obtener segunda página
        response = client.get(
            "/api/v1/tasks?page=2&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5
    
    def test_get_task_by_id(self, client, auth_headers, test_task):
        """Test: Obtener tarea por ID"""
        response = client.get(
            f"/api/v1/tasks/{test_task.id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == test_task.title
    
    def test_get_task_not_found(self, client, auth_headers):
        """Test: Obtener tarea inexistente retorna 404"""
        response = client.get("/api/v1/tasks/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Tarea no encontrada"
    
    def test_update_task_success(self, client, auth_headers, test_task):
        """Test: Actualizar tarea exitosamente"""
        update_data = {
            "title": "Título actualizado",
            "status": "in_progress"
        }
        
        response = client.put(
            f"/api/v1/tasks/{test_task.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
    
    def test_update_task_partial(self, client, auth_headers, test_task):
        """Test: Actualización parcial de tarea"""
        original_title = test_task.title
        update_data = {"status": "completed"}
        
        response = client.put(
            f"/api/v1/tasks/{test_task.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == original_title  # No cambió
        assert data["status"] == "completed"  # Cambió
    
    def test_update_task_not_found(self, client, auth_headers):
        """Test: Actualizar tarea inexistente retorna 404"""
        response = client.put(
            "/api/v1/tasks/99999",
            json={"title": "Nuevo título"},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_success(self, client, auth_headers, test_task):
        """Test: Eliminar tarea exitosamente"""
        task_id = test_task.id
        
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que la tarea ya no existe
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_not_found(self, client, auth_headers):
        """Test: Eliminar tarea inexistente retorna 404"""
        response = client.delete("/api/v1/tasks/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestTaskBusinessLogic:
    """Tests para lógica de negocio de tareas"""
    
    def test_task_status_transitions(self, client, auth_headers):
        """Test: Transiciones de estado de tarea"""
        # Crear tarea
        response = client.post(
            "/api/v1/tasks",
            json={"title": "Tarea de flujo", "status": "pending"},
            headers=auth_headers
        )
        task_id = response.json()["id"]
        
        # pending -> in_progress
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"status": "in_progress"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "in_progress"
        
        # in_progress -> completed
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"status": "completed"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "completed"
    
    def test_task_title_max_length(self, client, auth_headers):
        """Test: Título de tarea respeta longitud máxima"""
        long_title = "a" * 256  # Excede el máximo de 255
        
        response = client.post(
            "/api/v1/tasks",
            json={"title": long_title},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
