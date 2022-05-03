from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings

config = get_settings()

engine=create_engine(
    "postgresql://{}:{}@{}/{}".format(
        config.POSTGRES_USERNAME, 
        config.POSTGRES_PASSWORD,
        config.POSTGRES_HOST,
        config.POSTGRES_SCHEMA
    ),
    echo=True
)

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)