from pydantic import BaseModel
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum
from datetime import datetime
from config.database import Session, engine, Base
from models.models import User, Category, TaskStatus, Task
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn
from typing import Optional
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
app = FastAPI()

app.title = "Gestion de Tareas"
app.version = "1.0"
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            try:
                data = validate_token(credentials.credentials)
                db = Session()  
                user_exists = db.query(User).filter(User.username == data['username']).first() is not None
                if not user_exists:
                    raise HTTPException(status_code=403, detail="Invalid credentials")
                return data  
            finally:
                db.close()  
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

class UserCreate(BaseModel):
    username: str
    password: str
    profile_image: Optional[str] = None


@app.get("/")
def hello():
    return "Hello World"

#USUARIOS
@app.post("/sign-up",response_model=UserCreate)
def create_user(user: UserCreate):
    nuevo_usuario = User(username=user.username, password=user.password, profile_image=user.profile_image)
    db=Session()
    db.add(nuevo_usuario)
    db.commit()
    
    return {"username": nuevo_usuario.username, "profile_image": nuevo_usuario.profile_image, "password": nuevo_usuario.password}

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/sign-in")
def login(user: UserLogin):
    db=Session()
    usuario=db.query(User).filter(User.username == user.username).first()
    if user.username == usuario.username and user.password == usuario.password:
        global usuario_final
        usuario_final = usuario.id
        token: str = create_token(user.dict())
        response_content = {"token": token, "usuario_id": usuario.id}
        return JSONResponse(status_code=200, content=response_content)
        
#CATEGORIAS
class CategoryCreate(BaseModel):
    name: str
    description: str

@app.post("/categories" ,dependencies=[Depends(JWTBearer())])
def create_category(category: CategoryCreate):
    db=Session()
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"No se pudo crear la categoría. Error: {str(e)}")
    return {"name": db_category.name, "id": db_category.id}

@app.delete("/categories/{category_id}",dependencies=[Depends(JWTBearer())])
def delete_category(category_id: int):
    db=Session()
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_category)
    db.commit()
    return {"status": "Eliminado"}

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

@app.get("/get_categories",dependencies=[Depends(JWTBearer())] )
def list_categories():
    db=Session()
    categories=db.query(Category).all()
    return categories



#TAREAS
class TaskCreate(BaseModel):
    text: str
    due_date: datetime
    category_id: str

@app.post("/tareas", dependencies=[Depends(JWTBearer())])
def create_task(task: TaskCreate, payload: dict = Depends(JWTBearer())):
    db=Session()
    username = payload.get("usuario_id")
    #user=db.query(User).filter(User.username==username).first()
    user_id=usuario_final

    #category = db.query(Category).filter(Category.id == task.category_id).first()
    #if category:
    #    category=category.id

    if not user_id:
        raise HTTPException(status_code=403, detail=user_id)
    db_task = Task(text=task.text, due_date=task.due_date, category_id=task.category_id, user_id=user_id)
    db.add(db_task)
    try:
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo crear la tarea. Error: {}".format(str(e)))
    return {"task": "Task created", "id": db_task.id}

class TaskUpdate(BaseModel):
    text: str = None
    due_date: datetime = None
    status: str = None

@app.put("/tareas/{id}", dependencies=[Depends(JWTBearer())])
def update_task(id: int, task_update: TaskUpdate):
    db=Session()
    task = db.query(Task).filter(Task.id == id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return {"task": "Task updated", "id": id, "updated_fields": task_data}

@app.delete("/tareas/{id}",dependencies=[Depends(JWTBearer())])
def delete_task(task_id: int):
    db=Session()
    db_category = db.query(Task).filter(Task.id == task_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(db_category)
    db.commit()
    return {"status": "Eliminado"}

@app.get("/tareas/usuario/{id}",dependencies=[Depends(JWTBearer())])
def list_tasks_user(id: int):
    db=Session()
    return db.query(Task).filter(Task.user_id == id).all()

@app.get("/tareas/{id}",dependencies=[Depends(JWTBearer())])
def list_tasks_user(id:int):
    db=Session()
    return db.query(Task).filter(Task.id == id).all()




