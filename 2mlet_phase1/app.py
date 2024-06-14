from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'message':'This is the root endpoint'}
