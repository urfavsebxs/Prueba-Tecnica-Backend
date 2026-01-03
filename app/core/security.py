# Funciones de seguridad
# Hash de passwords y creación de tokens JWT

from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuración de bcrypt para hashear passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica si la password ingresada coincide con el hash guardado en la BD
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Hashea una password para guardarla en la BD
    # NUNCA guardar passwords en texto plano!
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    # Crea un token JWT para el usuario
    # El token expira después de cierto tiempo por seguridad
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Si no se especifica, usa el default de 30 min del config
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    # Firma el token con la SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt