from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import SessionLocal
from backend.models import Task, Base
from backend.database import engine
from datetime import datetime


Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskCreate(BaseModel):
    title: str
    priority: int
    deadline: str

class TaskRead(BaseModel):
    id: int
    title: str
    priority: int
    deadline: str
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        priority=task.priority,
        deadline=task.deadline
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/completed")
def delete_completed_tasks(db: Session = Depends(get_db)):
    db.query(Task).filter(Task.completed == True).delete()
    db.commit()
    return {"message": "All completed tasks deleted."}


@router.get("/", response_model=list[TaskRead])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.put("/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    db.refresh(task)
    return task
