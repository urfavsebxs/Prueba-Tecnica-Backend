# Modelo de Tarea para la base de datos

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class TaskStatus(str, enum.Enum):
    # Estados que puede tener una tarea
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"

    # Campos de la tarea
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)  # Indexado para búsquedas
    description = Column(String, nullable=True)  # Opcional
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,  # Por defecto es pending
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
