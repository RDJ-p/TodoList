from pydantic import BaseModel
class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False
class TodoCreate(TaskBase):
    pass    
class ToDoResponse(TaskBase):
    id: int
    class Config:
        orm_mode = True