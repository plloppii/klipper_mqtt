from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings

config = get_settings()
postgres_url = "postgresql://{}:{}@{}/{}".format(
        config.POSTGRES_USERNAME, 
        config.POSTGRES_PASSWORD,
        config.POSTGRES_HOST,
        config.POSTGRES_SCHEMA
    )

engine = create_engine(postgres_url, echo=True)

SessionLocal=sessionmaker(bind=engine)