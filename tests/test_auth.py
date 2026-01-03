"""
Tests para autenticación
"""
import pytest
from fastapi import status


class TestAuthentication:
    """Suite de pruebas para autenticación"""
    
    def test_login_success(self, client, test_user):
        """Test: Login exitoso con credenciales válidas"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self, client):
        """Test: Login falla con email inválido"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "noexiste@example.com", "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Email o contraseña incorrectos"
    
    def test_login_invalid_password(self, client, test_user):
        """Test: Login falla con contraseña incorrecta"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Email o contraseña incorrectos"
    
    def test_login_inactive_user(self, client, db_session, test_user):
        """Test: Login falla con usuario inactivo"""
        test_user.is_active = False
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Usuario inactivo"
    
    def test_access_protected_endpoint_without_token(self, client):
        """Test: Acceso denegado a endpoint protegido sin token"""
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_invalid_token(self, client):
        """Test: Acceso denegado con token inválido"""
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": "Bearer token_invalido"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_valid_token(self, client, auth_headers):
        """Test: Acceso permitido con token válido"""
        response = client.get("/api/v1/tasks", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
