# Endpoints de tareas
# CRUD completo: listar, crear, actualizar, eliminar
# Todos requieren autenticación (token JWT)

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.core.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[TaskOut])
def read_tasks(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    # GET /tasks - Lista todas las tareas con paginación
    skip = (page - 1) * page_size
    tasks = task_service.get_tasks(db, skip=skip, limit=page_size)
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # GET /tasks/{id} - Obtiene una tarea específica
    task = task_service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # POST /tasks - Crea una nueva tarea
    return task_service.create_task(db, obj_in=task_in)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # PUT /tasks/{id} - Actualiza una tarea
    task = task_service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task_service.update_task(db, db_obj=task, obj_in=task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # DELETE /tasks/{id} - Elimina una tarea
    task = task_service.delete_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return None
