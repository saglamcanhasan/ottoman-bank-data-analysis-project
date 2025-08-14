import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers.router import router
from fastapi.middleware.cors import CORSMiddleware

# load port
load_dotenv()
port = int(os.getenv("PORT"))

# create app
app = FastAPI()

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5001",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(router, prefix="/api")

# start server
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=port, reload=True)