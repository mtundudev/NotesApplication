from fastapi import FastAPI
from app.api.router import auth,note,user,uploads
from app.core.config import settings

app=FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(note.router)
app.include_router(uploads.router)


@app.get("/health",tags=["Health"])
def checkheatth():
    return{
        "message":"welcome to note application"
    }