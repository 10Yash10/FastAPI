from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database url with name and password along with port number and database name
db_url = "postgresql://postgres:12345678@localhost:5432/demodb"

# creating engine, basically creating the connecitvity object.
engine = create_engine(db_url)

# creating session for our application
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# create dependency injection for connection start and close
def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()

