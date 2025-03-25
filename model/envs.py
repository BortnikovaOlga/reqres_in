# APP_URL=http://127.0.0.1:8008
# HOST=127.0.0.1
# PORT=8008
# DATABASE_ENGINE=postgresql+psycopg2://postgres:example@localhost:5434/postgres
from pydantic import BaseModel


class Envs(BaseModel):
    app_url: str
    host: str
    port: int
    db_engine: str
    test_username:str
    test_password:str
