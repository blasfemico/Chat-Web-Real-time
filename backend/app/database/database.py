from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dante20121@localhost:5432/evasoft"
  # Para desarrollo, se puede usar PostgreSQL en producción

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def init_db():
    # Importa todos los modelos para asegurarse de que se crean las tablas en la base de datos
    import app.database.models
    Base.metadata.create_all(bind=engine)
