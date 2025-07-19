# TaskOptima AI Agent

> **An AI-powered task management system**

---

## 🚀 Overview

TaskOptima helps users create, organize, and prioritize tasks using a local LLaMA-based AI. Features:

* Add, view, complete, and delete tasks via REST API
* AI-driven recommendations: next task, breakdowns, weekly schedules
* Conversation history of AI interactions
* Containerized setup with Docker Compose

---

## 📋 Contents

```
AI_AGENT/
├── backend/           # FastAPI backend service
├── frontend/          # React.js frontend application
├── models/            # Downloaded LLaMA model weights (GGUF)
├── .env               # Example environment variables file
└── docker-compose.yaml# Orchestrates backend, frontend, and PostgreSQL
```

---

## 🛠 Prerequisites

* **Git** installed on your machine
* **Python 3.12+** and **pip**
* **Node.js** (v18+) and **npm**
* **PostgreSQL** (if running locally)
* **Docker & Docker Compose** (optional, recommended for isolation)

---
### System Build Tools (for LLaMA inference)

- **CMake** (≥3.18)  
- **C/C++ Compiler**  
  - **Linux/macOS**: `build-essential` (GCC) or `clang`  
  - **Windows**: Visual Studio C++ Build Tools (workloads: “Desktop Development with C++”)  


## ⚙️ Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/taskoptima.git
cd taskoptima
```

### 2. Environment Variables

1. Create `.env` file:

2. Open `.env` and set:

   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/taskoptima_db
   LLAMA_MODEL_PATH=./models/phi-2.Q4_K_M.gguf
   ```

### 3. Backend Installation & Run

```bash
python -m venv venv                 # create virtual env
# Activate the venv:
venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

# Initialize database (ensure PostgreSQL is running):
# Create database 'taskoptima_db' via psql or pgAdmin

#starts the backend app
uvicorn backend.main:app --reload
```

* **Backend URL**: [http://localhost:8000](http://localhost:8000)
* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Frontend Installation & Run

```bash
cd ../frontend
npm install
npm start
```

* **Frontend URL**: [http://localhost:3000](http://localhost:3000)

---

## 🐳 Docker Setup (Optional)

Ensure Docker Desktop is running.

```bash
# From project root
docker-compose up --build
```

* **Services**:

  * **db**: PostgreSQL on port 5432
  * **backend**: FastAPI on port 8000
  * **frontend**: React on port 3000

To stop and remove containers:

```bash
docker-compose down
```

---

## 📦 Usage

1. **Add Task**: via UI or POST `/tasks/`
2. **View Tasks**: GET `/tasks/`
3. **Complete Task**: PUT `/tasks/{id}/complete`
4. **Delete Completed**: DELETE `/tasks/completed`
5. **Ask AI**: POST `/agent/query` with `{ "question": "..." }`
6. **Weekly Plan**: POST `/agent/schedule`
7. **History**: GET `/agent/history`

---

## 🔮 Future Enhancements

* User authentication & multi-tenant support
* Calendar and notification integration
* Advanced analytics dashboard
* Mobile-responsive UI

---

