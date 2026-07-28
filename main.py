from fastapi import FastAPI

app = FastAPI()

#get - print information about the API
#put - update information about the API
#post - create new information about the API
#delete - delete information about the API
#python -m uvicorn main:app --port 8000 --reload

#Stage 0 — Hello, server
@app.get("/")

def index():
    return {"message": "Hello World!"}

#Stage 1 — Create a new endpoint

myAPI = {1 : 
         {"name": "Task API",
           "version": "1.0",
             "endpoints": ["/tasks"]}
}

@app.get("/api")
def get_api(api_id: int):
    return myAPI[api_id]

@app.get("/health")
def health():
    return {"status": "OK"}

#Sage 2 — Create a new endpoint to return a list of tasks

tasks = [
    {"id": 1, "title": "Task 1", "COOK DINNER": "This is task 1", "completed": False},
    {"id": 2, "title": "Task 2", "WASH CLOTHES": "This is task 2", "completed": True},
    {"id": 3, "title": "Task 3", "CLEAN HOUSE": "This is task 3", "completed": False}
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id == 0 or task_id > len(tasks):
        return { "error": f"Task {task_id} not found" }
    else:
        return tasks[task_id -1]


            