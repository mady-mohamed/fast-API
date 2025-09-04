from fastapi import FastAPI

app = FastAPI(title="Blog API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}