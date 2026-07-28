from fastapi import FastAPI

app = FastAPI()

#get - print information about the API
#put - update information about the API
#post - create new information about the API
#delete - delete information about the API

#Stage 0 — Hello, server
@app.get("/")

def index():
    return {"message": "Hello World!"}