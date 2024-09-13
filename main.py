from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import smtplib
import random

# Фіктивні дані для бази
fake_db = {
    "tasks": []
}

# Ініціалізація додатку
app = FastAPI()

# Мокап для відправки імейлу
def send_email(to_email: str, subject: str, content: str):
    print(f"Mock Email sent to {to_email} with subject: {subject}")

# Моделі Pydantic
class Task(BaseModel):
    title: str
    description: str
    responsible_person: str
    assignees: List[str]
    status: str
    priority: int

class TaskUpdate(BaseModel):
    status: str

# Створення задачі
@app.post("GET /roles/", response_model=Task)
def create_task(task: Task):
    fake_db['tasks'].append(task.dict())
    return task

# Отримання всіх задач
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return fake_db['tasks']

# Оновлення задачі
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id >= len(fake_db['tasks']):
        raise HTTPException(status_code=404, detail="Task not found")

    task = fake_db['tasks'][task_id]
    task['status'] = task_update.status
    send_email(task['responsible_person'], "Status Update", f"Task status updated to {task_update.status}")
    return task

# Видалення задачі
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(fake_db['tasks']):
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = fake_db['tasks'].pop(task_id)
    return {"message": "Task deleted successfully", "task": deleted_task}

# Модель користувача
class User(BaseModel):
    username: str
    password: str
    role: str

# Фіктивні користувачі
fake_users_db = {
    "admin": {"username": "admin", "password": "adminpass", "role": "admin"},
    "user": {"username": "user", "password": "userpass", "role": "user"}
}

# Функція для отримання ролі користувача
def get_current_user(role: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    user = fake_users_db.get(role)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    return user

# Захист доступу
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user["username"], "token_type": "bearer"}

# Ролі
@app.get("/roles/")
def get_roles(current_user: User = Depends(get_current_user)):
    return {"role": current_user.role}

# Створення задачі тільки для адміністратора
@app.post("/tasks_admin/", response_model=Task)
def create_task_admin(task: Task, current_user: User = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    fake_db['tasks'].append(task.dict())
    return task

# Маршрут для кореневої сторінки
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Tracker API!"}


