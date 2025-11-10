import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from time import sleep

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/imobiliaria")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# wait for DB to be ready (simple)
def wait_for_db(hostname="db", port=5432, tries=10, delay=1.0):
    import socket
    for i in range(tries):
        try:
            s = socket.create_connection((hostname, port), timeout=1)
            s.close()
            logger.info("Database reachable")
            return True
        except Exception:
            logger.info("Aguardando banco de dados ficar pronto (tentativa %d)...", i+1)
            sleep(delay)
    return False

wait_for_db()

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()