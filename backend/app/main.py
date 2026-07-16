from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI Backend"
    }

@app.get("/employees")
def employees():
    return [
        {
            "id": 1,
            "name": "John",
            "department": "IT"
        },
        {
            "id": 2,
            "name": "Alice",
            "department": "HR"
        }
    ]
