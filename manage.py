from fastapi import FastAPI
import uvicorn
from app.views import api
from app.auth_views import *

app = FastAPI()




app.include_router(api, prefix="/api")
app.include_router(auth, prefix="/auth", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("manage:app", host="127.0.0.1", port=8001, reload=True)
