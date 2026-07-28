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