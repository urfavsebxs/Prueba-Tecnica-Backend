# Servicio de tareas
# Maneja toda la lógica CRUD de tareas

from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    # Obtiene lista de tareas con paginación
    # skip = cuántos saltar, limit = cuántos traer
    return db.query(Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    # Busca una tarea por ID
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, obj_in: TaskCreate):
    # Crea una nueva tarea en la BD
    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        status=obj_in.status
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_task(db: Session, db_obj: Task, obj_in: TaskUpdate):
    # Actualiza una tarea existente
    # Solo actualiza los campos que vengan en obj_in
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_task(db: Session, task_id: int):
    # Elimina una tarea de la BD
    obj = db.query(Task).get(task_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj