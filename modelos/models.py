from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum  # Cambio aquí
import datetime
from enum import Enum
from config.database import Base

#Base = declarative_base()

class TaskStatus(Enum):
    NOT_STARTED = "Sin Empezar"
    STARTED = "Empezada"
    FINISHED = "Finalizada"

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime)
    status = Column(SQLAlchemyEnum(TaskStatus))  
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    category = relationship("Category")
    owner = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    profile_image = Column(String)
    tasks = relationship("Task", back_populates="owner")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)



