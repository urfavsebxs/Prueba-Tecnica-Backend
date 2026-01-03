"""
Tests para funcionalidad de seguridad
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)
from app.core.config import settings


class TestPasswordHashing:
    """Tests para hash de contraseñas"""
    
    def test_password_hash_and_verify(self):
        """Test: Hash de contraseña y verificación"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # El hash no debe ser igual a la contraseña
        assert hashed != password
        
        # Verificar que la contraseña es correcta
        assert verify_password(password, hashed) is True
    
    def test_verify_wrong_password(self):
        """Test: Verificación falla con contraseña incorrecta"""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        assert verify_password("wrong_password", hashed) is False
    
    def test_different_passwords_different_hashes(self):
        """Test: Contraseñas diferentes generan hashes diferentes"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2


class TestJWTTokens:
    """Tests para tokens JWT"""
    
    def test_create_access_token(self):
        """Test: Crear token de acceso"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        # El token debe ser un string no vacío
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decodificar y verificar contenido
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        assert payload["sub"] == "test@example.com"
        assert "exp" in payload
    
    def test_token_expiration(self):
        """Test: Token tiene tiempo de expiración correcto"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar que el token tiene campo de expiración
        assert "exp" in payload
        
        # Verificar que la expiración es en el futuro
        import time
        current_time = time.time()
        assert payload["exp"] > current_time
    
    def test_token_with_custom_expiration(self):
        """Test: Token con tiempo de expiración personalizado"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(hours=1)
        
        token = create_access_token(data, expires_delta=expires_delta)
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar que el token tiene campo de expiración
        assert "exp" in payload
        
        # Verificar que la expiración es aproximadamente 1 hora en el futuro
        import time
        current_time = time.time()
        expected_exp = current_time + 3600  # 1 hora
        # Permitir 2 minutos de diferencia
        assert abs(payload["exp"] - expected_exp) < 120
    
    def test_invalid_token(self):
        """Test: Token inválido genera excepción"""
        from jose import JWTError
        
        with pytest.raises(JWTError):
            jwt.decode(
                "invalid_token",
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
