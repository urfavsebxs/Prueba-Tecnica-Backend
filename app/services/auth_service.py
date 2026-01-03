# Servicio de autenticación
# Funciones para validar usuarios y crear nuevos

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.schemas.user import UserCreate

def authenticate(db: Session, email: str, password: str) -> User | None:
    # Valida email y password, retorna el usuario si es correcto
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    # Busca un usuario por email
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    # Crea un nuevo usuario en la BD
    # Importante: hashea la password antes de guardar
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user