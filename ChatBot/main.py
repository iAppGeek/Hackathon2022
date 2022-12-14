from fastapi import FastAPI

app = FastAPI()

# install requirements
import initalise

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
