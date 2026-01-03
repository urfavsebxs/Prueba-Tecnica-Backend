"""
Script de prueba para la API de Tareas
Ejecutar con: python test_api.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api():
    print("=== Prueba de API de Tareas ===\n")
    
    # 1. Login
    print("1. Autenticación...")
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✓ Login exitoso. Token: {token[:30]}...\n")
    else:
        print(f"✗ Error en login: {response.status_code}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Crear tarea
    print("2. Crear nueva tarea...")
    task_data = {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea creada desde el script de prueba",
        "status": "pending"
    }
    response = requests.post(
        f"{BASE_URL}/tasks",
        json=task_data,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        task = response.json()
        task_id = task["id"]
        print(f"✓ Tarea creada con ID: {task_id}")
        print(f"  Título: {task['title']}")
        print(f"  Estado: {task['status']}\n")
    else:
        print(f"✗ Error creando tarea: {response.status_code} - {response.text}")
        return
    
    # 3. Listar tareas
    print("3. Listar todas las tareas...")
    response = requests.get(
        f"{BASE_URL}/tasks",
        headers=headers
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✓ Total de tareas: {len(tasks)}")
        for task in tasks:
            print(f"  - [{task['id']}] {task['title']} ({task['status']})")
        print()
    else:
        print(f"✗ Error listando tareas: {response.status_code}\n")
    
    # 4. Actualizar tarea
    print("4. Actualizar tarea a 'in_progress'...")
    update_data = {
        "status": "in_progress"
    }
    response = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json=update_data,
        headers=headers
    )
    
    if response.status_code == 200:
        task = response.json()
        print(f"✓ Tarea actualizada: {task['status']}\n")
    else:
        print(f"✗ Error actualizando tarea: {response.status_code}\n")
    
    # 5. Obtener tarea específica
    print("5. Obtener tarea por ID...")
    response = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        task = response.json()
        print(f"✓ Tarea obtenida:")
        print(f"  ID: {task['id']}")
        print(f"  Título: {task['title']}")
        print(f"  Descripción: {task['description']}")
        print(f"  Estado: {task['status']}")
        print(f"  Creada: {task['created_at']}\n")
    else:
        print(f"✗ Error obteniendo tarea: {response.status_code}\n")
    
    # 6. Eliminar tarea
    print("6. Eliminar tarea...")
    response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    
    if response.status_code == 204:
        print(f"✓ Tarea eliminada exitosamente\n")
    else:
        print(f"✗ Error eliminando tarea: {response.status_code}\n")
    
    # 7. Verificar eliminación
    print("7. Verificar que la tarea fue eliminada...")
    response = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    
    if response.status_code == 404:
        print("✓ Tarea no encontrada (eliminación confirmada)\n")
    else:
        print(f"✗ La tarea todavía existe: {response.status_code}\n")
    
    print("=== Pruebas completadas ===")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar al servidor.")
        print("  Asegúrate de que el servidor esté corriendo en http://127.0.0.1:8000")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
