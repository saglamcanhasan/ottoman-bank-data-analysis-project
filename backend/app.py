import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers.router import router

# load port
load_dotenv()
port = int(os.getenv("PORT"))

# create app
app = FastAPI()

# middleware
app.include_router(router, prefix="/api")

# start server
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=port, reload=True)