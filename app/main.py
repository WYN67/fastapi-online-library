from fastapi import FastAPI

app = FastAPI(title="Online Library")

@app.get("/")
async def root():
    return {"message": "Welcome to Online Library"}
