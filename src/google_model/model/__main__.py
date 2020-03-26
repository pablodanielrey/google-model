

def create_tables():

    import os
    from sqlalchemy import create_engine

    from .entities import Base
    from .entities.Google import GoogleLog

    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['GOOGLE_DB_USER'],
        os.environ['GOOGLE_DB_PASSWORD'],
        os.environ['GOOGLE_DB_HOST'],
        os.environ['GOOGLE_DB_PORT'],
        os.environ['GOOGLE_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)


create_tables()
