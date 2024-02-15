from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from credentials import username, password, database, host, port


Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}', echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all of the models
    # This will associate the models with the Base metadata
    import models
    Base.metadata.create_all(bind=engine)

    # for testing purposes only (delete tables and records)
    Base.metadata.drop_all(engine)


    # Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
    Base.metadata.create_all(engine)
