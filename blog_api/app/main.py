from fastapi import FastAPI

app = FastAPI(title="Blog API")

@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"message": "Welcome to the Blog API"}
=======
    return {"message": "Welcome to Blog API"}
>>>>>>> acb66af4bd347b565b79e4f6cd07e69b54a14261
