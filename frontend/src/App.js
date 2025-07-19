import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState(1);
  const [deadline, setDeadline] = useState("");
  const [tasks, setTasks] = useState([]);
  const [history, setHistory] = useState([]);
  const [question, setQuestion] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [schedule, setSchedule] = useState("");
  const [loadingSchedule, setLoadingSchedule] = useState(false);

  const today = new Date();
  const overdueTasks = tasks.filter(task => !task.completed && new Date(task.deadline) < today);
  const urgentTasks = tasks.filter(task =>
    !task.completed &&
    ((new Date(task.deadline) - today) / (1000 * 60 * 60 * 24) <= 1 || task.priority === 1)
  );

  // Load tasks from backend
  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    if (aiResponse) {
      axios.get(`${API_BASE}/agent/history`)
        .then(res => setHistory(res.data));
    }
  }, [aiResponse]);

  const fetchTasks = () => {
    axios.get(`${API_BASE}/tasks/`).then(res => setTasks(res.data));
  };

  // Add a new task
  const handleAddTask = (e) => {
    e.preventDefault();
    axios.post(`${API_BASE}/tasks/`, { title, priority, deadline })
      .then(res => {
        setTasks([...tasks, res.data]);
        setTitle(""); setPriority(1); setDeadline("");
      });
  };

  // Remove all completed tasks
  const handleRemoveCompleted = () => {
    axios.delete(`${API_BASE}/tasks/completed`)
      .then(() => fetchTasks());
  };


  const handleSuggestSchedule = () => {
  setLoadingSchedule(true);
  setSchedule("Loading...");
  axios.post(`${API_BASE}/agent/schedule`)
    .then(res => {
      setSchedule(res.data.schedule);
      setLoadingSchedule(false);
    })
    .catch(() => {
      setSchedule("Error retrieving schedule.");
      setLoadingSchedule(false);
    });
};

  // Ask the AI agent
  const handleAskAgent = (e) => {
    e.preventDefault();
    setAiResponse("Loading...");
    axios.post(`${API_BASE}/agent/query`, { question })
      .then(res => setAiResponse(res.data.response))
      .catch(() => setAiResponse("Error communicating with agent."));
  };

  // Mark task as completed
  const handleCompleteTask = (id) => {
    axios.put(`${API_BASE}/tasks/${id}/complete`)
      .then(() => fetchTasks());
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8">

          <div className="card shadow mb-4">
            <div className="card-body">
              <h2 className="card-title mb-3">Add New Task</h2>
              <form className="row g-2 align-items-end" onSubmit={handleAddTask}>
                <div className="col">
                  <input className="form-control" value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" required />
                </div>
                <div className="col">
                  <input className="form-control" type="number" value={priority} onChange={e => setPriority(e.target.value)} placeholder="Priority" min="1" max="5" required />
                </div>
                <div className="col">
                  <input className="form-control" type="date" value={deadline} onChange={e => setDeadline(e.target.value)} required />
                </div>
                <div className="col">
                  <button className="btn btn-success" type="submit">Add</button>
                </div>
              </form>
            </div>
          </div>

          <div className="card shadow mb-4">
            <div className="card-body">
              {overdueTasks.length > 0 && (
              <div className="alert alert-danger">
              <b>Overdue tasks:</b> {overdueTasks.map(t => t.title).join(", ")}
              </div>
              )}
              {urgentTasks.length > 0 && (
                <div className="alert alert-warning">
                  <b>Urgent tasks:</b> {urgentTasks.map(t => t.title).join(", ")}
                </div>
              )}

              <h2 className="card-title mb-3">Current Tasks</h2>
              <button className="btn btn-outline-danger mb-3" onClick={handleRemoveCompleted}>Remove Completed Tasks</button>
              <ul className="list-group">
                {tasks.length === 0 && <li className="list-group-item text-muted">No tasks yet.</li>}
                {tasks.map(task =>
                  <li key={task.id} className={`list-group-item d-flex justify-content-between align-items-center ${task.completed ? "list-group-item-secondary" : ""}`}>
                    <div>
                      <b>{task.title}</b> (Priority: {task.priority}, Deadline: {task.deadline}) {" "}
                      {task.completed && <span className="badge bg-success">Completed</span>}
                    </div>
                    {!task.completed && (
                      <button className="btn btn-sm btn-outline-primary" onClick={() => handleCompleteTask(task.id)}>
                        Mark as Done
                      </button>
                    )}
                  </li>
                )}
              </ul>
            </div>
          </div>
          
          <div className="my-4">
            <button
              className="btn btn-outline-info"
              onClick={handleSuggestSchedule}
              disabled={loadingSchedule}
            >
              Suggest Weekly Plan
            </button>
          </div>

          {schedule && (
            <div className="alert alert-secondary mt-3">
              <b>Your Weekly Plan:</b>
              <pre style={{whiteSpace: "pre-wrap"}}>{schedule}</pre>
            </div>
          )}


          <div className="card shadow">
            <div className="card-body">
              <h2 className="card-title mb-3">Ask TaskOptima AI</h2>
              <form className="row g-2 align-items-end" onSubmit={handleAskAgent}>
                <div className="col-9">
                  <input className="form-control" value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask a productivity question..." required />
                </div>
                <div className="col-3">
                  <button className="btn btn-info w-100" type="submit">Ask</button>
                </div>
              </form>
              <div className="mt-4 p-3 bg-light rounded shadow-sm">
                <b>AI Response:</b>
                <div className="mt-2">{aiResponse}</div>
              </div>
            </div>
          </div>

          <div className="card shadow mt-4">
            <div className="card-body">
              <h2 className="card-title mb-3">Conversation History</h2>
              <ul className="list-group">
                {history.map((h, i) => (
                  <li key={i} className="list-group-item">
                    <b>You:</b> {h.question} <br/>
                    <b>AI:</b> {h.response} <br/>
                    <small>{new Date(h.timestamp).toLocaleString()}</small>
                  </li>
                ))}
              </ul>
            </div>
          </div>


        </div>
      </div>
    </div>
    
  );
}

export default App;
