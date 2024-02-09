"""
Sets up postgresql database connection pool.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker, Session

db_user: str = os.environ.get("db_user") or ""
db_port: int = int(os.environ.get("db_port") or 5432)
db_name: str = os.environ.get("db_name") or ""
db_host: str = os.environ.get("db_host") or ""
db_password: str = os.environ.get("db_password") or ""


engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    future=True,
    pool_pre_ping=True,
    pool_size=50,  # pgbouncer pool size = 50
    pool_timeout=100,  # pgbouncer pool timeout = 120
)


session_maker = sessionmaker(engine)


def get_db() -> Session:
    return session_maker()
