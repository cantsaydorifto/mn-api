from fastapi import FastAPI
from routers import homepage, actor, search, video

app = FastAPI()

app.include_router(homepage.router)
app.include_router(search.router)
app.include_router(actor.router)
app.include_router(video.router)


@app.get("/")
async def home():
    return {"message": "Hello World!"}
