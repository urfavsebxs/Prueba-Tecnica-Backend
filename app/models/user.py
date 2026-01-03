# Modelo de Usuario para la base de datos

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    # Campos del usuario
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # Para login
    hashed_password = Column(String, nullable=False)  # Password hasheada, nunca en texto plano
    is_active = Column(Boolean, default=True, nullable=False)  # Si el usuario puede entrar
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

