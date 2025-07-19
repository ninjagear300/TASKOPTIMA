from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Task
from pydantic import BaseModel
from backend.models import Conversation
from backend.utils.langchain_utils import ask_phi2, taskoptima_prompt

router = APIRouter(prefix="/agent")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AgentQuery(BaseModel):
    question: str
    
@router.post("/schedule")
def suggest_schedule(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.completed == False).all()
    task_list = [
        {"title": t.title, "priority": t.priority, "deadline": t.deadline}
        for t in tasks
    ]
    prompt = (
        "You are a productivity AI. Here is the user's current task list:\n" +
        "\n".join([f"- {t['title']} (priority: {t['priority']}, deadline: {t['deadline']})" for t in task_list]) +
        "\nSuggest a 7-day plan for completing these tasks, balancing priorities and deadlines."
    )
    response = ask_phi2(prompt)
    return {"schedule": response}

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.timestamp.desc()).limit(20).all()
    return [{"question": c.question, "response": c.response, "timestamp": c.timestamp} for c in conversations]

    

@router.post("/query")
def query_agent(query: AgentQuery, db: Session = Depends(get_db)):
    # 1. Load all incomplete tasks from the database
    tasks = db.query(Task).filter(Task.completed == False).all()

    # 2. Format tasks for the prompt
    task_list = [
        {"title": t.title, "priority": t.priority, "deadline": t.deadline}
        for t in tasks
    ]

    # 3. Create the prompt for the LLM
    prompt = taskoptima_prompt(task_list, query.question)

    # 4. Get the AI response
    response = ask_phi2(prompt)
    conv = Conversation(question=query.question, response=response)
    db.add(conv)
    db.commit()
    return {"response": response}
