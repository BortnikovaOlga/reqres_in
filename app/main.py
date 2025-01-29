import os
import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.database.engine import create_db_and_tables
from router import login, status, users


app = FastAPI()
app.include_router(status.router)
app.include_router(login.router)
app.include_router(users.router)

# @app.on_event("startup")

if __name__ == "__main__":
    import uvicorn

    add_pagination(app)
    create_db_and_tables()
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
