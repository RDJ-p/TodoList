from fastapi import FastAPI, HTTPException,Depends
from database import SessionLocal, engine, Base
import models
from sqlalchemy.orm import Session
from schemas import TodoCreate, ToDoResponse
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or ["http://localhost:3000"] for React dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/tasks/", response_model=ToDoResponse)
def add_task(task: TodoCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task 
@app.get("/task/all",response_model=list[ToDoResponse])
def get_all(db:Session=Depends(get_db)):
    tasks=db.query(models.Task).all()
    return tasks
@app.get("/tasks/{task_id}", response_model=ToDoResponse)
def get_by_id(task_id:int, db:Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==task_id).first()
    return task
@app.put("/tasks/{task_id}", response_model=ToDoResponse)
def update(task_id:int, task:TodoCreate, db:Session=Depends(get_db)):
    existing_task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key,value in task.dict().items():
        setattr(existing_task, key, value)
    db.commit()
    db.refresh(existing_task)   
    return existing_task
@app.delete("/tasks/{task_id}")
def delete(task_id:int, db:Session=Depends(get_db)):
    db_task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
@app.get("/tasks/name/{task_name}", response_model=ToDoResponse)
def get_by_name(task_name: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.title == task_name).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
