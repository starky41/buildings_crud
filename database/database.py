from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from credentials import username, password, database, host, port
from sqlalchemy.exc import IntegrityError


Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}', echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from database.populate_database import populate_database

    
    # for testing purposes only (delete tables and records)
    # Base.metadata.drop_all(engine)

    # Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
    Base.metadata.create_all(engine)
    try:
        populate_database()
    except IntegrityError as e:
        print("THE VALUES YOU ARE TRYING TO ADD WITH populate_database() already exist in the table")
        pass

    
