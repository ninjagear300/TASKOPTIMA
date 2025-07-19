import os
from dotenv import load_dotenv
from langchain_community.llms import LlamaCpp
from datetime import datetime

def get_urgent_overdue_tasks(tasks):
    today = datetime.today().date()
    urgent = []
    overdue = []
    for task in tasks:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        if not task.get("completed", False):
            if deadline < today:
                overdue.append(task)
            elif (deadline - today).days <= 1 or task["priority"] == 1:
                urgent.append(task)
    return urgent, overdue


load_dotenv()
model_path = os.getenv("LLAMA_MODEL_PATH")

llm = LlamaCpp(
    model_path=model_path,
    n_ctx=1024,         # context window, adjust if needed
    temperature=0.1,    # low temp = more predictable answers
    max_tokens=512,
    n_threads=4         # adjust based on your CPU
)



def taskoptima_prompt(task_list: list, user_question: str) -> str:
    urgent, overdue = get_urgent_overdue_tasks(task_list)
    alerts = ""
    if overdue:
        alerts += "⚠️ Overdue Tasks:\n" + "\n".join([f"- {t['title']} (deadline: {t['deadline']})" for t in overdue]) + "\n"
    if urgent:
        alerts += "⚡ Urgent Tasks:\n" + "\n".join([f"- {t['title']} (priority: {t['priority']}, deadline: {t['deadline']})" for t in urgent]) + "\n"
    tasks = "\n".join([
        f"{i+1}. Task: {task['title']}\n   Priority: {task['priority']}\n   Deadline: {task['deadline']}"
        for i, task in enumerate(task_list)
    ])
    context = (
        "You are TaskOptima, an advanced AI assistant for productivity.\n"
        + alerts +
        "Here is the user's current task list:\n"
        f"{tasks}\n\n"
        "Instructions:\n"
        "- If the user asks for a schedule, planning, or how to organize their week, suggest a daily plan that balances deadlines and priorities, and mention which tasks should be done each day. Group tasks by urgency and due date.\n"
        "- If the user asks about a large or complex task (like 'write a report', 'prepare a presentation', or 'finish a project'), suggest breaking it into smaller, manageable subtasks and give concrete examples if possible.\n"
        "- If any tasks are overdue or urgent, alert the user clearly.\n"
        "- Recommend what to focus on and why.\n"
        f"User's question: {user_question}\n"
        "TaskOptima's reply:"
    )
    return context






def ask_phi2(prompt: str) -> str:
    return llm(prompt)
