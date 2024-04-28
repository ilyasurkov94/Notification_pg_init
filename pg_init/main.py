import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists, create_database

from config import settings
from models import Base


def main():
    pg_conn_url = settings.postgres.conn_url

    if not database_exists(pg_conn_url):
        logging.info("Database doesn't exist")
        try:
            create_database(pg_conn_url)
            logging.info("Database successfully created")
        except Exception as e:
            logging.error(f'{e.__class__.__name__}\n{str(e)}')
            return
    else:
        logging.info("Database already exists")

    engine = create_engine(pg_conn_url)
    inspector = inspect(engine)
    db_tables = inspector.get_table_names()

    if not db_tables:
        logging.info("No existed tables")
        Base.metadata.create_all(bind=engine)
        logging.info("Tables successfully created")
    else:
        logging.info("Tables already exists")


if __name__ == '__main__':
    main()