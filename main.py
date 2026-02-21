from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Voting API running"}
