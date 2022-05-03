from database import Base,engine
from models import Print_History

print("Creating database ....")

Base.metadata.create_all(engine)