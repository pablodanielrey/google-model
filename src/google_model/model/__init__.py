import os
import logging
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

EMAILS_API_URL = os.environ['EMAILS_API_URL']

@contextlib.contextmanager
def open_session():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['GOOGLE_DB_USER'],
        os.environ['GOOGLE_DB_PASSWORD'],
        os.environ['GOOGLE_DB_HOST'],
        os.environ['GOOGLE_DB_PORT'],
        os.environ['GOOGLE_DB_NAME']
    ), echo=False)    
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

